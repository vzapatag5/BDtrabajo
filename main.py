from frontend.main_ui import MainUI

def main():
    try:
        app = MainUI()
        app.show_login()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
    finally:
        input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()