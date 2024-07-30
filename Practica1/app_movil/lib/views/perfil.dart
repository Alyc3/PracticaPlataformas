import 'package:app_movil/controllers/Service.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';

class Perfil extends StatefulWidget {
  @override
  _PerfilState createState() => _PerfilState();
}

class _PerfilState extends State<Perfil> {
  final TextEditingController nombreController = TextEditingController();
  final TextEditingController apellidoController = TextEditingController();
  final TextEditingController correoController = TextEditingController();
  final TextEditingController claveController = TextEditingController();
  List<Map<String, dynamic>> cuentas = [];
  final _formKey = GlobalKey<FormState>();
  

  @override
  void initState() {
    super.initState();
    // Aquí puedes llamar a una función para obtener los datos del correo
    _cargarDatoscorreo();
  }

  void _cargarDatoscorreo() async {
    try {
      Services service = Services();
      final value = await service.getPersona();
      print(value.datos);
      if (value.code == '200' && value.datos != null) {
        Map<String, dynamic> persona = value.datos;
        setState(() {
          nombreController.text = persona['nombres'];
          apellidoController.text = persona['apellidos'];
          cuentas = List<Map<String, dynamic>>.from(persona['cuenta']);
          if (cuentas.isNotEmpty) {
            correoController.text = cuentas[0]['correo'];
          }
        });
      }
    } catch (e) {
      print("Error al cargar la persona: $e");
    }
  }

  void guardarPersona(BuildContext context) async {
    FToast fToast = FToast();
    fToast.init(context);

    try {
      Services service = Services();
      Services personaService = Services();
      final persona = await personaService.getPersona();
      print(persona.datos);

      // Obtener el external_id de la cuenta
      String cuentaExternalId = '';
      if (persona.datos != null &&
          persona.datos['cuenta'] != null &&
          persona.datos['cuenta'].isNotEmpty) {
        cuentaExternalId = persona.datos['cuenta'][0]['external_id'];
      }

      Map<String, dynamic> data = {
        "nombres": nombreController.text,
        "apellidos": apellidoController.text,
        "correo": correoController.text,
        "clave": claveController.text,
      };
      print(cuentaExternalId);

      final value = await service.guardarPersona(cuentaExternalId, data);
      print(value.code);
      if (value.code == '200') {
        fToast.showToast(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.deepPurpleAccent,
              borderRadius: BorderRadius.circular(25),
              boxShadow: [],
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: const [
                Icon(Icons.check_circle_outline, color: Colors.white),
                SizedBox(width: 12),
                Text("Datos guardados correctamente",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                    )),
              ],
            ),
          ),
          gravity: ToastGravity.BOTTOM,
          toastDuration: const Duration(seconds: 2),
        );
        await Future.delayed(const Duration(seconds: 2), () {
          Navigator.pushNamed(context, '/Dashboard');
        });
      } else {
        fToast.showToast(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.red,
              borderRadius: BorderRadius.circular(25),
              boxShadow: [
                BoxShadow(
                  color: Colors.red.shade600,
                  spreadRadius: 3,
                  blurRadius: 5,
                  offset: Offset(0, 0), // Cambios de posición de la sombra
                ),
              ],
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: const [
                Icon(Icons.error_outline, color: Colors.white),
                SizedBox(width: 12),
                Text("Error al guardar los datos",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                    )),
              ],
            ),
          ),
          gravity: ToastGravity.BOTTOM,
          toastDuration: const Duration(seconds: 2),
        );
      }

    } catch (e) {
      fToast.showToast(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          decoration: BoxDecoration(
            color: Colors.red,
            borderRadius: BorderRadius.circular(25),
            boxShadow: [
              BoxShadow(
                color: Colors.red.shade600,
                spreadRadius: 3,
                blurRadius: 5,
                offset: Offset(0, 0), // Cambios de posición de la sombra
              ),
            ],
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: const [
              Icon(Icons.error_outline, color: Colors.white),
              SizedBox(width: 12),
              Text("Error al guardar la persona",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                  )),
            ],
          ),
        ),
        gravity: ToastGravity.BOTTOM,
        toastDuration: const Duration(seconds: 2),
      );
      print("Error al guardar la persona: $e");
    }
  }

  void _guardarPerfil() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      guardarPersona(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Perfil'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: <Widget>[
              TextFormField(
                controller: nombreController,
                decoration: InputDecoration(labelText: 'Nombre'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor ingrese su nombre';
                  }
                  return null;
                },
               
              ),
              TextFormField(
                controller: apellidoController,
                decoration: InputDecoration(labelText: 'Apellido'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor ingrese su apellido';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: correoController,
                decoration: InputDecoration(labelText: 'Correo'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor ingrese su correo';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: claveController,
                decoration: InputDecoration(labelText: 'Clave'),
                obscureText: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor ingrese su clave';
                  }
                  return null;
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _guardarPerfil,
                child: Text('Guardar'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}