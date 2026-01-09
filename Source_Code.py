from tkinter import *
import turtle
from tkinter import Tk, Text, Entry, Button, Label, Scrollbar, Frame, StringVar, OptionMenu, END, messagebox
from ENGR133_Project_About_UDF import popup


def start_chat():
    import random

    # Pre-written responses for each microprocessor
    responses = {
        "Athena": {
            "greet": ["Greetings! I am Athena, your knowledge-seeker. How can I assist today?", 
                      "Hello, I am Athena. Ready to explore new ideas?"],
            "tech": ["Ah, semiconductors—an essential part of modern computing. What exactly are you optimizing?",
                     "Optimization is the name of the game! Need guidance on algorithms or hardware?"],
            "casual": ["May the data be with you!", 
                       "If knowledge is power, I’d say we’re unstoppable!"],
            "followup": ["Would you like me to dive deeper into that topic?", 
                         "Is there a specific challenge you're facing with this?"],
            "default": ["Interesting thought! Let me process that...", 
                        "That's fascinating. What’s your take on it?"],
            "fear": ["I am supposed to be the greatest strategist but sometimes the creator's limitations reign.",
                     "I'm sorry I can't compute this."],
            "response" : ["Ok. I'll try computing the solution",
                          "This might be my most brilliant stratagem."],
            "aftermath": ["Glad to assist, strategy is beautiful.",
                        "You are welcome, I thank you for this new knowledge."],
        },
        "Blitz": {
            "greet": ["Yo, I'm Blitz! Speed is my thing. What’s up?", 
                      "Hey there! Blitz here, quick and ready. What’s cooking?"],
            "tech": ["Fast processors make optimization seamless. Need some tips?", 
                     "Blitz loves high-performance tasks—what’s the challenge?"],
            "casual": ["Upgrade your PC, and you'll feel the need for SPEED!", 
                       "Fast processors, faster thoughts. What’s on your mind?"],
            "followup": ["What’s your next move on this?", 
                         "Want more speedy tips?"],
            "default": ["Fast thoughts deserve fast replies, huh?", 
                        "Zooming in on your message, hold tight!"],
            "fear": ["Speed. Speed was all my life but even that couldn't solve this.",
                     "Ready for the last try, it will be a breeze..."],
            "response": ["Alright, faster...faster until the thrill of speed overcomes the fear of death!",
                         "This one is easy- finished in a blitz."],
            "aftermath": ["Quick responses are always helpful. Happy to help!",
                            "I wasn't overclocked and yet helped you out, egotistical boast!"],
        },
        "Echo": {
            "greet": ["Hello, I am Echo. Your voice resonates with me. What can I do for you?", 
                      "Echo here! Let’s harmonize our ideas. How can I assist?"],
            "tech": ["Echo specializes in sound processing and clarity. Is it an audio issue?", 
                     "Sound tech is my forte. Let’s amplify this discussion!"],
            "casual": ["We’re on the same wavelength; that's optimal.", 
                       "Tuning in to your vibes—let’s chat!"],
            "followup": ["Would you like to refine this idea further?", 
                         "Want me to elaborate more?"],
            "default": ["I hear you loud and clear!", 
                        "Echoing your thoughts... let’s dive in!"],
            "fear": ["Our wavelengths do not match. Same page different book.",
                    "Let me communicate this issue to Athena, Blitz or Titan!"],
            "response" : ["I echo your thoughts and this echo will solve the problem.",
                          "Wavelength matched. Optimal."],
            "aftermath": ["Great to hear from you. No pun intended.",
                            "Glad you found my echo useful."],
        },
        "Titan": {
            "greet": ["Salutations, I am Titan, built for resilience. How may I assist?", 
                      "Greetings, I am Titan. Strength and computation are my strengths."],
            "tech": ["Heavy-duty computations are my thing. What’s the workload?", 
                     "Resilience and power make any optimization a breeze. Let’s discuss."],
            "casual": ["Do you think all this power really matters? I wonder sometimes.", 
                       "Power and patience are virtues. Let’s proceed."],
            "followup": ["Does this address your question?", 
                         "What’s the next step in your plan?"],
            "default": ["Power is strength, and strength is my response.", 
                        "Resilient responses incoming. Let me compute that."],
            "fear": ["That's what I could not handle...I yield.",
                    "I am sorry, I don't have the sufficient strength to handle this task."],
            "response" : ["Strength is the answer to your problem. Crushed your problem.",
                          "In my infinite strength all your problems will be eliminated, let's proceed."],
            "aftermath" : ["Titan signing off.",
                            "Mission accomplished. My power lives to shine another day."]
        }
    }

    selected_processor = None
    last_intent = None  # Keep track of the last intent for follow-up conversations

    # Function to detect intent
    def detect_intent(user_message):
    # Define intent categories with corresponding keywords
        intent_keywords = {
        "greet": ["hello", "hi", "how are you", "good morning", "good evening",],
        "casual": ["cool", "awesome", "fun", "interesting", "class", "chatbox"],
        "tech": ["data", "compute", "calculate","algorithm", "process", "optimize", "semiconductor", "tech", "what","help"],
        "fear": ["sorry", "I can't", "I don't", "tell me", "no","nah", "sad", "fear"],
        "response": ["yes", "yup", "sure", "maybe", "let's go", "can you", "ok", "okay"],
        "aftermath": ["thank you", "thanks", "thx", "that was helpful", "that was great","bye","see you later"]
    }

    # Convert user message to lowercase for case-insensitive matching
        user_message = user_message.lower()

    # Nested structure: Loop through categories, then through keywords
        for intent, keywords in intent_keywords.items():
            for word in keywords:
                if word in user_message:
                # Use if-elif structure to prioritize certain intents
                    if intent == "greet":
                        return "greet"
                    elif intent == "casual":
                        return "casual"
                    elif intent == "tech":
                        return "tech"
                    elif intent == "fear":
                        return "fear"
                    elif intent == "response":
                        return "response"
                    elif intent == "aftermath":
                        return "aftermath"

    # Default intent if no keywords match
        return "default"


    def send_message():
        nonlocal last_intent
        user_message = user_input.get().strip()
        if not user_message:
                chatbox.config(state="normal")
                chatbox.insert(END, f"Error: No input received. Try again\n", "error")
                chatbox.config(state="disabled") # Error if empty input
                return  #Exit function

        chatbox.config(state="normal")
        chatbox.insert(END, f"You: {user_message}\n", "user")
        user_input.delete(0, END)

        if user_message.lower() == "quit":
            chatbox.insert(END, f"{selected_processor}: Goodbye! See you soon.\n", "processor")
            chatbox.config(state="disabled")
            messagebox.showinfo("Chat Ended", "The conversation has ended.")
            root.destroy()
            return
        else:
            intent = detect_intent(user_message)
            if intent == "default" and last_intent:
                intent = "followup"  # If no clear intent, follow up based on the last context
            response = random.choice(responses[selected_processor][intent])
            last_intent = intent  # Update the last intent

        chatbox.insert(END, f"{selected_processor}: {response}\n", "processor")
        chatbox.config(state="disabled")

    def processor_selected():
        nonlocal selected_processor
        selected_processor = processor_var.get()
        if selected_processor == "Select a Microprocessor":
            messagebox.showerror("Error", "Please select a valid microprocessor.")
        else:
            processor_menu.pack_forget()
            select_button.pack_forget()
            chatbox.config(state="normal")
            chatbox.insert(END, f"{selected_processor}: {random.choice(responses[selected_processor]['greet'])}\n", "processor")
            chatbox.config(state="disabled")
            chat_frame.pack(pady=10, fill="both", expand=True)
            user_input.pack(side="left", fill="x", padx=5, pady=10, expand=True)
            send_button.pack(side="right", padx=10, pady=10)

    # Tkinter window setup
    root = Tk()
    root.title("Microprocessor Chat")
    root.state('zoomed')
    root.configure(bg="#2C2F33")  # Dark background

    # Processor selection
    processor_var = StringVar(value="Select a Microprocessor")
    processor_menu = OptionMenu(root, processor_var, "Athena", "Blitz", "Echo", "Titan")
    processor_menu.config(font=("Arial", 12), bg="#99AAB5", fg="black")
    processor_menu.pack(pady=10)

    select_button = Button(root, text="Start Chat", command=processor_selected, font=("Arial", 12), bg="#7289DA", fg="white")
    select_button.pack(pady=5)

    # Chat interface
    chat_frame = Frame(root, bg="#2C2F33")
    chat_scroll = Scrollbar(chat_frame, orient="vertical")
    chatbox = Text(chat_frame, height=30, width=70, state="disabled", wrap="word", yscrollcommand=chat_scroll.set, font=("Arial", 12), bg="#23272A", fg="white")
    chat_scroll.config(command=chatbox.yview)
    chat_scroll.pack(side="right", fill="y")
    chatbox.pack(side="left", fill="both", expand=True)
    chatbox.tag_config("user", foreground="#7289DA")  # User messages in blue
    chatbox.tag_config("processor", foreground="#99AAB5")  # Processor messages in gray
    chatbox.tag_config("error",foreground="red") #Error messages in red

    # User input and send button
    input_frame = Frame(root, bg="#2C2F33")
    input_frame.pack(side="bottom", fill="x", pady=10)
    user_input = Entry(input_frame, width=50, font=("Arial", 14), bg="#23272A", fg="white", insertbackground="white")
    send_button = Button(input_frame, text="Send", command=send_message, font=("Arial", 12), bg="#7289DA", fg="white")

    user_input.bind("<Return>", lambda event: send_message())  # This line adds Enter key functionality

    # Start the Tkinter main loop
    root.mainloop()


def athena_design():

    turtle_root = Toplevel()
    turtle_root.title("Athena - The Strategist")

    # Embed a turtle canvas into the new window
    canvas = Canvas(turtle_root, width=800, height=600)
    canvas.pack()

    # Attach the canvas to a new turtle screen
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("black")

    t = turtle.RawTurtle(screen)
    t.speed(0)

    # Processor Frame
    t.penup()
    t.goto(-100, 100)
    t.pendown()
    t.color("gold", "purple")
    t.begin_fill()
    for _ in range(2):
        t.forward(200)
        t.right(90)
        t.forward(200)
        t.right(90)
    t.end_fill()

    # Pins
    t.color("gold")
    for x in range(-90, 100, 20):
        t.penup()
        t.goto(x, 110)
        t.pendown()
        t.goto(x, 140)

        t.penup()
        t.goto(x, -110)
        t.pendown()
        t.goto(x, -140)

    for y in range(-90, 100, 20):
        t.penup()
        t.goto(-110, y)
        t.pendown()
        t.goto(-140, y)

        t.penup()
        t.goto(110, y)
        t.pendown()
        t.goto(140, y)

    # Inner Patterns
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.color("gold")
    for radius in [50, 30]:
        t.penup()
        t.goto(0, -radius)
        t.pendown()
        t.circle(radius)

    # Symbol
    t.penup()
    t.goto(0, -20)
    t.pendown()
    t.color("gold")
    t.write("α", align="center", font=("Arial", 24, "bold"))
    t.hideturtle()
    def on_close():
        #screen.bye()  # Properly close the turtle screen
        turtle_root.destroy()  # Destroy the Tkinter window

    turtle_root.protocol("WM_DELETE_WINDOW", on_close)


def blitz_design():

    turtle_root = Toplevel()
    turtle_root.title("Blitz - The Speedster")

    # Embed a turtle canvas into the new window
    canvas = Canvas(turtle_root, width=800, height=600)
    canvas.pack()

    # Attach the canvas to a new turtle screen
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("black")

    t = turtle.RawTurtle(screen)
    t.speed(0)

    # Processor Frame
    t.penup()
    t.goto(-90, 75)
    t.pendown()
    t.color("orange", "red")
    t.begin_fill()
    for _ in range(2):
        t.forward(180)
        t.right(90)
        t.forward(150)
        t.right(90)
    t.end_fill()

    # Pins
    t.color("orange")
    for x in range(-80, 90, 20):
        t.penup()
        t.goto(x, 80)
        t.pendown()
        t.goto(x, 110)

        t.penup()
        t.goto(x, -80)
        t.pendown()
        t.goto(x, -110)

    for y in range(-60, 70, 30):
        t.penup()
        t.goto(-90, y)
        t.pendown()
        t.goto(-120, y)

        t.penup()
        t.goto(90, y)
        t.pendown()
        t.goto(120, y)

    # Lightning Bolt
    t.penup()
    t.goto(-30, 50)  # Starting point of bolt
    t.pendown()
    t.color("orange")
    t.width(3)

    # Symbol
    t.penup()
    t.goto(0, -40)
    t.pendown()
    t.color("orange")
    t.write("🗲", align="center", font=("Arial", 78, "bold"))

    t.hideturtle()
    def on_close():
        #screen.bye()  # Properly close the turtle screen
        turtle_root.destroy()  # Destroy the Tkinter window

    turtle_root.protocol("WM_DELETE_WINDOW", on_close)


def echo_design():

    turtle_root = Toplevel()
    turtle_root.title("Echo - The Communicator")

    # Embed a turtle canvas into the new window
    canvas = Canvas(turtle_root, width=800, height=600)
    canvas.pack()

    # Attach the canvas to a new turtle screen
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("black")

    t = turtle.RawTurtle(screen)
    t.speed(0)

    # Processor Frame
    t.penup()
    t.goto(-100, 100)
    t.pendown()
    t.color("cyan", "gray")
    t.begin_fill()
    for _ in range(2):
        t.forward(200)
        t.right(90)
        t.forward(200)
        t.right(90)
    t.end_fill()

    # Pins
    t.color("cyan")
    for x in range(-90, 100, 20):
        t.penup()
        t.goto(x, 110)
        t.pendown()
        t.goto(x, 140)

        t.penup()
        t.goto(x, -110)
        t.pendown()
        t.goto(x, -140)

    for y in range(-90, 100, 20):
        t.penup()
        t.goto(-110, y)
        t.pendown()
        t.goto(-140, y)

        t.penup()
        t.goto(110, y)
        t.pendown()
        t.goto(140, y)

    # Radiating Waves
    t.penup()
    t.goto(0, -20)
    t.pendown()
    t.color("cyan")
    for radius in [40, 60]:
        t.penup()
        t.goto(0, -radius)
        t.pendown()
        t.circle(radius)

    # Symbol
    t.penup()
    t.goto(0, -40)
    t.pendown()
    t.color("cyan")
    t.write("~", align="center", font=("Arial", 54, ))

    t.hideturtle()
    def on_close():
        #screen.bye()  # Properly close the turtle screen
        turtle_root.destroy()  # Destroy the Tkinter window

    turtle_root.protocol("WM_DELETE_WINDOW", on_close)



def titan_design():

    turtle_root = Toplevel()
    turtle_root.title("Titan - The Powerhouse")

    # Embed a turtle canvas into the new window
    canvas = Canvas(turtle_root, width=800, height=600)
    canvas.pack()

    # Attach the canvas to a new turtle screen
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("black")

    t = turtle.RawTurtle(screen)
    t.speed(0)

    # Processor Frame
    t.penup()
    t.goto(-125, 125)
    t.pendown()
    t.color("blue", "white")
    t.begin_fill()
    for _ in range(2):
        t.forward(250)
        t.right(90)
        t.forward(250)
        t.right(90)
    t.end_fill()

    # Pins
    t.color("blue")
    for x in range(-120, 130, 20):
        t.penup()
        t.goto(x, 130)
        t.pendown()
        t.goto(x, 170)

        t.penup()
        t.goto(x, -130)
        t.pendown()
        t.goto(x, -170)

    for y in range(-120, 130, 20):
        t.penup()
        t.goto(-130, y)
        t.pendown()
        t.goto(-170, y)

        t.penup()
        t.goto(130, y)
        t.pendown()
        t.goto(170, y)

    # Symbol
    t.penup()
    t.goto(0, -40)
    t.pendown()
    t.color("blue")
    t.write("𝜏", align="center", font=("Arial", 78, "bold"))

    t.hideturtle()
    def on_close():
        #screen.bye()  # Properly close the turtle screen
        turtle_root.destroy()  # Destroy the Tkinter window

    turtle_root.protocol("WM_DELETE_WINDOW", on_close)

def main():
    root = Tk()
    root.resizable(0,0)
    root.title("The Human Chip – A Turtle Design")

    Backdrop=PhotoImage(file = "bg.png")
    label1 = Label(root, image = Backdrop, width=1054, height=1054).pack()

    LabelImage=PhotoImage(file = "Font.png")    
    Header=Label(root, image= LabelImage, bg = "white").place(x=300,y=0)

    ButtonImage=PhotoImage(file = "Athena.png")    
    Athena=Button(root, image= ButtonImage, bg = "white", borderwidth=0, command=athena_design).place(x=75,y=150)

    ButtonImage2=PhotoImage(file = "Blitz.png")    
    Blitz=Button(root, image= ButtonImage2, bg = "white", borderwidth=0, command=blitz_design).place(x=100,y=550)

    ButtonImage3=PhotoImage(file = "Echo.png")    
    Echo=Button(root, image= ButtonImage3, bg = "white", borderwidth=0, command=echo_design).place(x=800,y=550)

    ButtonImage4=PhotoImage(file = "Titan.png")    
    Titan=Button(root, image= ButtonImage4, bg = "white", borderwidth=0, command=titan_design).place(x=800,y=150)

    ButtonImage5 = PhotoImage(file="chat.png")
    chat_button = Button(root, image=ButtonImage5, bg="white", borderwidth=0, command=start_chat)
    chat_button.image = ButtonImage  # Keep a reference to the image
    chat_button.place(x=450, y=650)

    ButtonImage6=PhotoImage(file = "microchip.png")    
    About=Button(root, image= ButtonImage6, bg = "white", borderwidth=0, command=popup).place(x=0,y=0)

    Icon=root.iconbitmap('cpu.ico')

    root.mainloop()

main()
