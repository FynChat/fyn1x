'''
Fyn1x: The AI Agents Orchestrator via CLI, FynChat and Telegram
'''
# Import some libs here

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pyfiglet import Figlet

console = Console()

def showBanner():
    figlet = Figlet(font="doom")
    banner = figlet.renderText("FYN1X")
    console.print(f"[bold magenta]{banner}[/bold magenta]")
    console.print(f"[dim]Multi-Agent code reviewer[/dim]\n")

def main():
    showBanner()
    console.print(Panel("Type [bold]exit[/bold] to quit\n",title="Fyn1x", border_style="purple"))

    while True:
        try:
            user_input = Prompt.ask("[bold purple]fyn1x[/bold purple]")
            if user_input.lower() in ("exit", "quit", "q"):
                break
            console.print(f"[green]You said:[/green] {user_input}\n")
        except (KeyboardInterrupt, EOFError):
            break
    console.print("[dim]Goodbye.[/dim]")

if __name__ == "__main__":
    main()
