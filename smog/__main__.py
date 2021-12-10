from smog import shell

if __name__ == "__main__":
    try:
        shell.run()
    except (KeyboardInterrupt, EOFError):
        shell.handle_command_line("quit")
