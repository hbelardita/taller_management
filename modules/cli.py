from .cli_manager import tool_management_menu, user_management_menu

def main_menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Gestión de Usuarios")
        print("2. Gestión de Herramientas y Máquinas")
        print("3. Gestión de Mantenimientos")
        print("4. Gestión de Asignaciones / Préstamos")
        print("0. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            user_management_menu()
        elif choice == '2':
            tool_management_menu()
        elif choice == '3':
            print("Funcionalidad 'Gestión de Mantenimientos' en desarrollo...")
        elif choice == '4':
            print("Funcionalidad 'Gestión de Asignaciones / Préstamos' en desarrollo...")
        elif choice == '0':
            print("Saliendo del programa. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")