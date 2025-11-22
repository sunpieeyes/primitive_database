def welcome():
    """
    Функция, отвечающая за первую проверочную логику:
    - выводит справку help
    - принимает команды 'help' и 'exit'
    """
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    while True:
        try:
            cmd = input("Введите команду: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            return

        if cmd == "":
            continue
        if cmd.lower() in ("exit", "quit"):
            print("До свидания!")
            return
        if cmd.lower() == "help":
            print()
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
            print()
            continue
        print(f"Неизвестная команда: {cmd}")
