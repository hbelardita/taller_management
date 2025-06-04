from modules.user_manager import create_user, get_all_users, format_user_info, get_user_by_id, update_user, delete_user, search_users
from modules.enums import UserType

def user_management_menu():
    while True:
        print("\n--- Menú de Gestión de Usuarios ---")
        print("1. Crear Usuario")
        print("2. Editar Usuario")
        print("3. Eliminar Usuario")
        print("4. Listar Usuarios")
        print("5. Buscar Usuario")
        print("0. Volver al Menú Principal")

        choice = input("Seleccione una opción: ")

        if choice == '1':
             
            user_data = prompt_for_user_data()
            if user_data:
                success, message, user_id = create_user(user_data)
                if success:
                    print(f"¡Éxito! {message}")
                else:
                    print(f"Error: {message}")
            else:
                print("Creación de usuario cancelada.")
        elif choice == '2':
            print("\n--- Editar Usuario ---")
            try:
                user_id = int(input("Ingrese el ID del usuario a editar: "))
            except ValueError:
                print("ID no válido. Por favor, ingrese un número.")
                continue

            user = get_user_by_id(user_id)
            if not user:
                print(f"Usuario con ID {user_id} no encontrado.")
                continue

            print("\nDatos actuales del usuario:")
            print(format_user_info(user))
            print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")

            updated_data = {}
            nombre = input(f"Nombre ({user.get('nombre', '')}): ").strip()
            if nombre: updated_data['nombre'] = nombre

            apellido = input(f"Apellido ({user.get('apellido', '')}): ").strip()
            if apellido: updated_data['apellido'] = apellido

            documento = input(f"Documento/Identificación ({user.get('documento', '')}): ").strip()
            if documento: updated_data['documento'] = documento
            
            # Tipo de usuario - manejo especial para validación
            while True:
                user_type_current = user.get('tipo_usuario', '')
                user_type_input = input(f"Tipo de Usuario ({user_type_current}) [Estudiante, Personal, Administrador]: ").strip()
                if not user_type_input: # Si se deja en blanco, mantener el actual
                    break
                elif UserType.is_valid(user_type_input):
                    updated_data['tipo_usuario'] = user_type_input
                    break
                else:
                    print("Tipo de usuario no válido. Por favor, elija uno de la lista.")
            
            # Email
            email_current = user.get('email', '')
            email = input(f"Email ({email_current}): ").strip()
            if email: updated_data['email'] = email
            elif email_current and not email: # Si se borra el email existente
                updated_data['email'] = ''

            # Campos específicos según el tipo de usuario (nuevo o actual)
            current_or_new_user_type = updated_data.get('tipo_usuario', user.get('tipo_usuario'))

            if current_or_new_user_type == UserType.ESTUDIANTE.value:
                curso_current = user.get('curso', '')
                curso = input(f"Curso/Grado ({curso_current}): ").strip()
                if curso: updated_data['curso'] = curso
                elif curso_current and not curso: updated_data['curso'] = ''

                talleres_current = ', '.join(user.get('talleres_inscritos', []))
                talleres = input(f"Talleres Inscritos ({talleres_current}) (separados por coma): ").strip()
                if talleres: updated_data['talleres_inscritos'] = [t.strip() for t in talleres.split(',') if t.strip()]
                elif talleres_current and not talleres: updated_data['talleres_inscritos'] = []

            elif current_or_new_user_type == UserType.PERSONAL.value:
                rol_current = user.get('rol', '')
                rol = input(f"Rol/Cargo ({rol_current}): ").strip()
                if rol: updated_data['rol'] = rol
                elif rol_current and not rol: updated_data['rol'] = ''

                departamento_current = user.get('departamento', '')
                departamento = input(f"Departamento/Área ({departamento_current}): ").strip()
                if departamento: updated_data['departamento'] = departamento
                elif departamento_current and not departamento: updated_data['departamento'] = ''

            if updated_data: 
                success, message = update_user(user_id, updated_data)
                if success:
                    print(f"¡Éxito! {message}")
                else:
                    print(f"Error: {message}")
            else:
                print("No se ingresaron datos para actualizar. Edición cancelada.")

        elif choice == '3':
            print("\n--- Eliminar Usuario ---")
            try:
                user_id = int(input("Ingrese el ID del usuario a eliminar: "))
            except ValueError:
                print("ID no válido. Por favor, ingrese un número.")
                continue

            user = get_user_by_id(user_id)
            if not user:
                print(f"Usuario con ID {user_id} no encontrado.")
                continue

            print(f"Está a punto de eliminar al siguiente usuario:\n{format_user_info(user)}")
            confirm = input("¿Está seguro que desea eliminar este usuario? (s/n): ").lower()

            if confirm == 's':
                success, message = delete_user(user_id)
                if success:
                    print(f"¡Éxito! {message}")
                else:
                    print(f"Error: {message}")
            else:
                print("Eliminación de usuario cancelada.")
        elif choice == '4':
            print("\n--- Listado de Usuarios ---")
            users = get_all_users()
            if users:
                for user in users:
                    print(format_user_info(user))
                    print("--------------------")
            else:
                print("No hay usuarios registrados en el sistema.")
        elif choice == '5':
            print("\n--- Buscar Usuario ---")
            search_term = input("Ingrese término de búsqueda (nombre, apellido, documento) o deje en blanco: ").strip()
            user_type = input("Ingrese tipo de usuario (Estudiante, Personal, Administrador) o deje en blanco: ").strip()
            course = input("Ingrese curso (solo para Estudiantes) o deje en blanco: ").strip()
            role = input("Ingrese rol (solo para Personal) o deje en blanco: ").strip()

            # Validar tipo de usuario si se ingresó
            if user_type and not UserType.is_valid(user_type):
                print("Tipo de usuario no válido. Por favor, elija uno de la lista.")
                continue

            found_users = search_users(search_term=search_term, user_type=user_type, course=course, role=role)

            if found_users:
                print("\n--- Resultados de la Búsqueda ---")
                for user in found_users:
                    print(format_user_info(user))
                    print("--------------------")
            else:
                print("No se encontraron usuarios con los criterios de búsqueda especificados.")
        elif choice == '0':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def tool_management_menu():
    while True:
        print("\n--- Menú de Gestión de Herramientas y Máquinas ---")
        print("1. Crear Herramienta")
        print("2. Editar Herramienta")
        print("3. Eliminar Herramienta")
        print("4. Listar Herramientas")
        print("5. Buscar Herramientas")
        print("0. Volver al Menú Principal")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            print("Funcionalidad 'Crear Herramienta' en desarrollo...")
        elif choice == '2':
            print("Funcionalidad 'Editar Herramienta' en desarrollo...")
        elif choice == '3':
            print("Funcionalidad 'Eliminar Herramienta' en desarrollo...")
        elif choice == '4':
            print("Funcionalidad 'Listar Herramientas' en desarrollo...")
        elif choice == '5':
            print("Funcionalidad 'Buscar Herramientas' en desarrollo...")
        elif choice == '0':
            print("Volviendo al Menú Principal...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def prompt_for_user_data() -> dict:
    print("\n--- Crear Nuevo Usuario ---")
    user_data = {}
    user_data['nombre'] = input("Nombre: ").strip()
    user_data['apellido'] = input("Apellido: ").strip()
    user_data['documento'] = input("Documento/Identificación: ").strip()

    while True:
        print("Tipos de Usuario disponibles:")
        for user_type in UserType.get_all_values():
            print(f"- {user_type}")
        user_type_input = input("Tipo de Usuario (Estudiante, Personal, Administrador): ").strip()
        if UserType.is_valid(user_type_input):
            user_data['tipo_usuario'] = user_type_input
            break
        else:
            print("Tipo de usuario no válido. Por favor, elija uno de la lista.")

    user_data['email'] = input("Email (opcional): ").strip()

    if user_data['tipo_usuario'] == UserType.ESTUDIANTE.value:
        user_data['curso'] = input("Curso/Grado: ").strip()
        talleres = input("Talleres Inscritos (separados por coma, opcional): ").strip()
        user_data['talleres_inscritos'] = [t.strip() for t in talleres.split(',') if t.strip()] if talleres else []
    elif user_data['tipo_usuario'] == UserType.PERSONAL.value:
        user_data['rol'] = input("Rol/Cargo: ").strip()
        user_data['departamento'] = input("Departamento/Área (opcional): ").strip()

    email = input("Email (opcional): ").strip()
    if email:
        user_data['email'] = email

    return user_data


