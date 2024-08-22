import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from pathlib import Path
from transformers import T5ForConditionalGeneration, T5Tokenizer
from generator import T5RAGWithLocalFiles
from retriever import read_local_file
from database import initialize_db, load_files_to_db, save_query, get_query_history
from rag import generate_answer

# Initialize database and load files into it
initialize_db()
load_files_to_db()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ToolTip:
    """A class for creating and managing tooltips in a Tkinter application."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event):
        """Display the tooltip window."""
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event):
        """Hide the tooltip window."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class PlaceholderEntry(ttk.Entry):
    """Custom Entry widget that clears placeholder text on click and restores it if the field is left empty."""
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']
        
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color

    def foc_in(self, *args):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self['foreground'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class Optimizer:
    """Handles the optimization process with the T5RAGWithLocalFiles model."""
    def __init__(self, generator, tokenizer):
        self.best_solution = None
        self.best_score = float('inf')
        self.running = False
        self.thread = None
        self.generator = generator
        self.tokenizer = tokenizer

    def start_optimization(self, query, file_path, update_callback, on_complete_callback, max_iterations=100):
        """Start the optimization process in a separate thread."""
        if self.running:
            logger.warning("Optimization already in progress.")
            return
        
        logger.info("Starting optimization process.")
        self.running = True
        self.thread = threading.Thread(
            target=self._optimize,
            args=(query, file_path, update_callback, on_complete_callback, max_iterations)
        )
        self.thread.daemon = True
        self.thread.start()

    def stop_optimization(self):
        """Stop the optimization process."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        logger.info("Optimization process stopped.")

    def _optimize(self, query, file_path, update_callback, on_complete_callback, max_iterations):
        """Run the optimization process."""
        try:
            t5_rag_local_model = T5RAGWithLocalFiles(self.generator, self.tokenizer)
            for iteration in range(1, max_iterations + 1):
                if not self.running:
                    break

                file_content = read_local_file(Path(file_path)) if file_path else ""
                inputs = self.tokenizer(query + file_content, return_tensors="pt", truncation=True, padding=True)
                solution_tensor = t5_rag_local_model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
                solution = self.tokenizer.decode(solution_tensor[0], skip_special_tokens=True)
                
                score = self._evaluate_solution(solution)
                logger.debug(f"Iteration {iteration}, Solution: {solution[:30]}..., Score: {score}")

                if score < self.best_score:
                    self.best_solution = solution
                    self.best_score = score
                    logger.info(f"New best solution found: {self.best_solution[:30]}... with score: {self.best_score}")
                    update_callback(self.best_solution, self.best_score, iteration)

                time.sleep(0.1)

            logger.info("Optimization process completed.")
            on_complete_callback(success=True)

        except Exception as e:
            logger.error(f"An error occurred during optimization: {e}")
            on_complete_callback(success=False)

    def _evaluate_solution(self, solution):
        """Evaluate the quality of the generated solution."""
        return len(solution) * random()  # Example evaluation based on the length of the generated solution

class OptimizationApp:
    """Main application class for handling optimization and query tasks."""
    def __init__(self, root):
        self.root = root
        self.root.title("MortyRAG")
        self.root.configure(bg="#1c1c1c")

        self.tokenizer = T5Tokenizer.from_pretrained("t5-base")
        self.generator = T5ForConditionalGeneration.from_pretrained("t5-base")
        self.optimizer = Optimizer(self.generator, self.tokenizer)
        
        self.query_history = []
        self._setup_styles()
        self.create_widgets()

    def _setup_styles(self):
        """Setup the styling for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 12), background='#1c1c1c', foreground='#9c27b0')
        style.configure('TButton', font=('Helvetica', 12), background='#9c27b0', foreground='#1c1c1c')
        style.configure('TFrame', background='#1c1c1c')
        style.configure('TProgressbar', thickness=20, troughcolor='#333333', background='#9c27b0')
        style.configure('TLabelframe', background='#1c1c1c', foreground='#9c27b0', relief='solid', borderwidth=1)
        style.configure('TLabelframe.Label', background='#1c1c1c', foreground='#9c27b0')

    def create_widgets(self):
        """Creates the GUI layout using a grid layout for better control."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        container = ttk.Frame(self.root, padding="10 10 10 10", style="TFrame")
        container.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        container.columnconfigure(0, weight=1)
        container.rowconfigure(list(range(14)), weight=1)

        title_label = ttk.Label(container, text="MortyRAG", font=('Helvetica', 24, 'bold'), style="TLabel", anchor='center')
        title_label.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=(0, 20))

        self.mode_var = tk.StringVar(value="Optimization")
        self.optimization_radio = ttk.Radiobutton(
            container, text="Optimization Mode", variable=self.mode_var, value="Optimization", command=self.toggle_mode, style="TRadiobutton"
        )
        self.optimization_radio.grid(column=0, row=1, sticky=tk.W, pady=5)
        ToolTip(self.optimization_radio, "Run the system in optimization mode to find the best solution.")

        self.query_radio = ttk.Radiobutton(
            container, text="Query Mode", variable=self.mode_var, value="Query", command=self.toggle_mode, style="TRadiobutton"
        )
        self.query_radio.grid(column=0, row=2, sticky=tk.W, pady=5)
        ToolTip(self.query_radio, "Run the system in query mode for single queries.")

        self.query_entry = PlaceholderEntry(container, placeholder="Enter your query here...", font=("Helvetica", 12))
        self.query_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.query_entry, "Type your query here before starting the process.")

        self.file_path_var = tk.StringVar()
        self.file_entry = PlaceholderEntry(container, textvariable=self.file_path_var, placeholder="Enter file path (optional)...", font=("Helvetica", 12))
        self.file_entry.grid(column=0, row=4, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.file_entry, "Optional: Provide a path to a file for additional context.")

        self.param_frame = ttk.LabelFrame(container, text="Model Parameters", padding="10", style="TLabelframe")
        self.param_frame.grid(column=0, row=5, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(self.param_frame, text="Max Length:", style="TLabel").grid(column=0, row=0, sticky=tk.W)
        self.max_length_var = tk.IntVar(value=200)
        self.max_length_entry = ttk.Entry(self.param_frame, textvariable=self.max_length_var, font=("Helvetica", 12))
        self.max_length_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.max_length_entry, "Set the maximum length of the generated text.")

        self.context_source_var = tk.StringVar(value="file")
        self.context_source_file_radio = ttk.Radiobutton(
            container, text="Context from Files", variable=self.context_source_var, value="file", style="TRadiobutton"
        )
        self.context_source_file_radio.grid(column=0, row=6, sticky=tk.W, pady=5)
        ToolTip(self.context_source_file_radio, "Use context from local files.")

        self.context_source_db_radio = ttk.Radiobutton(
            container, text="Context from Database", variable=self.context_source_var, value="database", style="TRadiobutton"
        )
        self.context_source_db_radio.grid(column=0, row=7, sticky=tk.W, pady=5)
        ToolTip(self.context_source_db_radio, "Use context from the database.")

        self.start_button = ttk.Button(container, text="Start", command=self.start_process)
        self.start_button.grid(column=0, row=8, pady=5)
        ToolTip(self.start_button, "Start the optimization or query process based on the selected mode.")

        self.stop_button = ttk.Button(container, text="Stop", command=self.stop_process, state=tk.DISABLED)
        self.stop_button.grid(column=0, row=9, pady=5)
        ToolTip(self.stop_button, "Stop the ongoing optimization process.")

        self.solution_label = ttk.Label(container, text="Best Solution: N/A", style="TLabel")
        self.solution_label.grid(column=0, row=10, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.solution_label, "Displays the best solution found during optimization or the query result.")

        self.score_label = ttk.Label(container, text="Best Score: N/A", style="TLabel")
        self.score_label.grid(column=0, row=11, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.score_label, "Displays the score of the best solution.")

        self.progress_label = ttk.Label(container, text="Progress: 0%", style="TLabel")
        self.progress_label.grid(column=0, row=12, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.progress_label, "Shows the progress of the optimization process.")

        self.progress_bar = ttk.Progressbar(container, orient="horizontal", mode="determinate", style="TProgressbar")
        self.progress_bar.grid(column=0, row=13, sticky=(tk.W, tk.E), pady=5)
        ToolTip(self.progress_bar, "Displays the progress bar during optimization.")

        self.status_label = ttk.Label(container, text="Status: Idle", style="TLabel")
        self.status_label.grid(column=0, row=14, sticky=(tk.W, tk.E), pady=10)
        ToolTip(self.status_label, "Shows the current status of the process.")

        self.history_button = ttk.Button(container, text="View History", command=self.view_history)
        self.history_button.grid(column=0, row=15, pady=5)
        ToolTip(self.history_button, "View the history of queries and results.")

    def toggle_mode(self):
        """Toggle between Optimization Mode and Query Mode."""
        mode = self.mode_var.get()
        if mode == "Query":
            self.stop_button.config(state=tk.DISABLED)
        elif mode == "Optimization":
            self.stop_button.config(state=tk.DISABLED if self.optimizer.running else tk.NORMAL)

    def start_process(self):
        """Handle the start of either the optimization or query process based on the selected mode."""
        query = self.query_entry.get().strip()
        file_path = self.file_path_var.get().strip()
        context_source = self.context_source_var.get()

        if not query or query == "Enter your query here...":
            messagebox.showerror("Input Error", "Please enter a valid query before starting.")
            return

        mode = self.mode_var.get()
        max_length = self.max_length_var.get()

        if mode == "Optimization":
            self.start_optimization(query, file_path, max_length, context_source)
        elif mode == "Query":
            self.start_query(query, file_path, max_length, context_source)

    def start_optimization(self, query, file_path, max_length, context_source):
        """Start the optimization process."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running Optimization...")
        self.progress_bar["value"] = 0

        self.optimizer.start_optimization(
            query, file_path, self.update_solution, self.on_optimization_complete, max_iterations=100
        )

    def start_query(self, query, file_path, max_length, context_source):
        """Handle a single query process."""
        try:
            self.status_label.config(text="Status: Processing Query...")
            self.start_button.config(state=tk.DISABLED)
            generated_text = generate_answer(query=query, file_path=Path(file_path) if file_path else None, max_length=max_length, context_source=context_source)
            self.show_query_result(generated_text)
            self.status_label.config(text="Status: Complete")
            self.start_button.config(state=tk.NORMAL)
        except Exception as e:
            logger.error(f"Error during query handling: {e}")
            messagebox.showerror("Query Error", "An error occurred during query processing.")
            self.status_label.config(text="Status: Error")
            self.start_button.config(state=tk.NORMAL)

    def stop_process(self):
        """Handle stopping the ongoing optimization process."""
        self.optimizer.stop_optimization()
        self.status_label.config(text="Status: Stopped")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_solution(self, solution, score, iteration):
        """Update the GUI with the new best solution and score during optimization."""
        self.solution_label.config(text=f"Best Solution: {solution[:50]}...")
        self.score_label.config(text=f"Best Score: {score:.4f}")
        self.progress_label.config(text=f"Progress: {iteration}%")
        self.progress_bar["value"] = iteration

    def on_optimization_complete(self, success):
        """Handle the completion of the optimization process."""
        if success:
            self.status_label.config(text="Status: Optimization Complete")
        else:
            self.status_label.config(text="Status: Error")
            messagebox.showerror("Optimization Error", "An error occurred during the optimization process.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def show_query_result(self, result_text):
        """Display the result of a query in a pop-up window."""
        result_window = tk.Toplevel(self.root)
        result_window.title("Query Result")
        result_window.geometry("400x300")

        result_label = tk.Label(result_window, text="Query Result:", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        result_textbox = tk.Text(result_window, wrap="word", font=("Helvetica", 12))
        result_textbox.insert("1.0", result_text)
        result_textbox.config(state=tk.DISABLED)
        result_textbox.pack(expand=True, fill="both", padx=10, pady=10)

    def view_history(self):
        """View query history stored in the SQLite database."""
        history = get_query_history()
        if history:
            history_str = "\n".join([f"{record[3]}: {record[1]} - {record[2]}" for record in history])
            messagebox.showinfo("Query History", history_str)
        else:
            messagebox.showinfo("Query History", "No history found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()