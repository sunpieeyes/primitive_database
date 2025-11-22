#!/usr/bin/env python3

def main():
    # Минимальное поведение: запуск движка и приветствие
    from src.primitive_db.engine import welcome
    welcome()

if __name__ == "__main__":
    main()
