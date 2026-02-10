from app import create_app

# Crear la aplicación usando la factoría
app = create_app()

# Configuraciones extra de desarrollo
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

if __name__ == '__main__':
    # Esto permite que el servidor se reinicie solo al guardar cambios
    app.run(debug=True, port=5000)