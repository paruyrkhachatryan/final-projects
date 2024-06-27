import tkinter as tk
from tkinter import messagebox, StringVar
import random

QUESTIONS = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Rome"], "answer": "Paris"},
    {"question": "Who wrote 'To Kill a Mockingbird'?", "options": ["Harper Lee", "J.K. Rowling", "Ernest Hemingway", "Mark Twain"], "answer": "Harper Lee"},
    {"question": "What is the largest planet in our solar system?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter"},
    {"question": "What is the chemical symbol for water?", "options": ["H2O", "O2", "CO2", "HO"], "answer": "H2O"},
    {"question": "Who painted the Mona Lisa?", "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "answer": "Leonardo da Vinci"},
    {"question": "What is the capital of Japan?", "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"], "answer": "Tokyo"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
    {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Jane Austen", "Charlotte Bronte", "Charles Dickens", "William Shakespeare"], "answer": "Jane Austen"},
    {"question": "What is the tallest mountain in the world?", "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"], "answer": "Mount Everest"},
    {"question": "Which ocean is the largest?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"},
    {"question": "What is the smallest country in the world?", "options": ["Monaco", "Nauru", "Vatican City", "San Marino"], "answer": "Vatican City"},
    {"question": "What is 5 * 2?", "options": ["3", "10", "12", "6"], "answer": "10"},
    {"question": "Who is the author of '1984'?", "options": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "J.R.R. Tolkien"], "answer": "George Orwell"},
    {"question": "What is the capital of Canada?", "options": ["Toronto", "Ottawa", "Vancouver", "Montreal"], "answer": "Ottawa"},
    {"question": "Which element has the chemical symbol 'O'?", "options": ["Oxygen", "Gold", "Osmium", "Oganesson"], "answer": "Oxygen"},
    {"question": "In which year did the Titanic sink?", "options": ["1905", "1912", "1921", "1930"], "answer": "1912"},
    {"question": "Who developed the theory of relativity?", "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"], "answer": "Albert Einstein"},
    {"question": "What is the currency of Japan?", "options": ["Yuan", "Won", "Yen", "Dollar"], "answer": "Yen"},
    {"question": "Which country hosted the 2016 Summer Olympics?", "options": ["China", "United Kingdom", "Brazil", "Russia"], "answer": "Brazil"},
]


class MillionaireGame(tk.Tk):
    """A class for the 'Who Wants to Be a Millionaire' game implemented with Tkinter."""

    def __init__(self):
        super().__init__()
        self.title("Who Wants to Be a Millionaire")
        self.geometry("600x400")
        self.nickname = None
        self.current_question = 0
        self.correct_answers = 0
        self.questions = random.sample(QUESTIONS, len(QUESTIONS))
        self.used_helps = {"50-50": False, "Phone a Friend": False, "Ask the Audience": False}

        self.show_nickname_input()

    def show_nickname_input(self):
        """Display the nickname input screen."""
        self.clear_frame()
        tk.Label(self, text="Enter your nickname:").pack(pady=10)
        self.nickname_entry = tk.Entry(self)
        self.nickname_entry.pack(pady=10)
        tk.Button(self, text="Start Game", command=self.start_game).pack(pady=10)

    def start_game(self):
        """Start the game after receiving the nickname."""
        self.nickname = self.nickname_entry.get()
        if not self.nickname or self.nickname.isspace():
            messagebox.showwarning("Warning", "Please enter a nickname")
        else:
            self.current_question = 0
            self.correct_answers = 0
            self.used_helps = {"50-50": False, "Phone a Friend": False, "Ask the Audience": False}
            self.show_question()

    def show_question(self):
        """Display the current question and answer options."""
        self.clear_frame()
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            tk.Label(self, text=question_data["question"]).pack(pady=10)

            self.option_var = StringVar()
            self.option_var.set(None)

            for option in question_data["options"]:
                tk.Radiobutton(self, text=option, variable=self.option_var, value=option).pack(pady=5)

            tk.Button(self, text="Submit Answer", command=self.check_answer).pack(pady=10)

            tk.Button(self, text="50-50", command=self.use_50_50).pack(side=tk.LEFT, padx=20)
            tk.Button(self, text="Phone a Friend", command=self.phone_a_friend).pack(side=tk.LEFT, padx=20)
            tk.Button(self, text="Ask the Audience", command=self.ask_the_audience).pack(side=tk.LEFT, padx=20)
        else:
            self.end_game()

    def check_answer(self):
        """Check the selected answer and move to the next question."""
        selected_option = self.option_var.get()
        if not selected_option:
            messagebox.showwarning("Warning", "Please select an answer")
            return

        correct_option = self.questions[self.current_question]["answer"]

        if selected_option == correct_option:
            self.correct_answers += 1

        self.current_question += 1
        self.show_question()

    def end_game(self):
        """Display the end game screen with the result."""
        self.clear_frame()
        tk.Label(self, text=f"Game Over! You answered {self.correct_answers} questions correctly.").pack(pady=10)
        tk.Button(self, text="Play Again", command=self.show_nickname_input).pack(pady=20)

    def use_50_50(self):
        """Use the 50-50 help to remove two incorrect options."""
        if not self.used_helps["50-50"]:
            self.used_helps["50-50"] = True
            correct_answer = self.questions[self.current_question]["answer"]
            options = self.questions[self.current_question]["options"]
            options_to_remove = random.sample([opt for opt in options if opt != correct_answer], 2)
            for child in self.winfo_children():
                if isinstance(child, tk.Radiobutton) and child.cget('text') in options_to_remove:
                    child.pack_forget()
        else:
            messagebox.showwarning("Warning", "50-50 help has already been used")

    def phone_a_friend(self):
        """Use the Phone a Friend help to get the correct answer."""
        if not self.used_helps["Phone a Friend"]:
            self.used_helps["Phone a Friend"] = True
            correct_answer = self.questions[self.current_question]["answer"]
            messagebox.showinfo("Phone a Friend", f"Your friend thinks the answer is {correct_answer}")
        else:
            messagebox.showwarning("Warning", "Phone a Friend help has already been used")

    def ask_the_audience(self):
        """Use the Ask the Audience help to get the correct answer."""
        if not self.used_helps["Ask the Audience"]:
            self.used_helps["Ask the Audience"] = True
            correct_answer = self.questions[self.current_question]["answer"]
            messagebox.showinfo("Ask the Audience", f"The audience thinks the answer is {correct_answer}")
        else:
            messagebox.showwarning("Warning", "Ask the Audience help has already been used")

    def clear_frame(self):
        """Clear all widgets from the current frame."""
        for widget in self.winfo_children():
            widget.pack_forget()


if __name__ == "__main__":
    app = MillionaireGame()
    app.mainloop()
