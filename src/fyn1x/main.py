'''
Fyn1x: The AI Agents Orchestrator via CLI, FynChat and Telegram
'''
# Import some libs here

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pyfiglet import Figlet
from ddgs import DDGS
from .parser import loads, dumps


console = Console()

def showBanner():
    figlet = Figlet(font="doom")
    banner = figlet.renderText("FYN1X")
    console.print(f"[bold magenta]{banner}[/bold magenta]")
    console.print(f"[dim]Multi-Agent code reviewer[/dim]\n")

'''
"$q" is the variable which gets user prompt and the keywords of it but for now we'll just accept simple requests
'''

def search(q):
    results = DDGS().text(q, max_results=2)
    parsed = results
    print("Parsed:")
    print(parsed)


    print("\nSerialized:")
    print(dumps(parsed, indent=2))


def main():
    showBanner()
    console.print(Panel("Type [bold]exit[/bold] to quit\n",title="Fyn1x", border_style="purple"))

    while True:
        try:
            user_input = Prompt.ask("[bold purple]fyn1x[/bold purple]")
            if user_input.lower() in ("exit", "quit", "q"):
                break
            console.print(f"[green]You said:[/green] {user_input}\n")
            search(user_input)
        except (KeyboardInterrupt, EOFError):
            break
    console.print("[dim]Goodbye.[/dim]")

if __name__ == "__main__":
    main()
