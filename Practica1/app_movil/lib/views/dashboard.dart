import 'package:app_movil/views/mapView.dart';
import 'package:app_movil/views/perfil.dart';
import 'package:app_movil/views/sucursales.dart';
import 'package:flutter/material.dart';

class Dashboard extends StatefulWidget {
  Dashboard({super.key});

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  Widget _currentWidget = MapView();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Color.fromARGB(255, 168, 140, 97),
              ),
              child: Text(
                'Tienda',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              leading: Icon(Icons.map),
              title: Text('Mapa'),
              onTap: () {
                // Actualiza el widget actual a MapView
                setState(() {
                  _currentWidget = MapView(); // Asegúrate de que MapView sea el nombre correcto de tu vista de mapa
                });
                // Cierra el drawer
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: Icon(Icons.account_circle),
              title: Text('Perfil'),
              onTap: () {
                // Actualiza el widget actual a Perfil
                setState(() {
                  _currentWidget = Perfil();
                });
                // Cierra el drawer
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: Icon(Icons.settings),
              title: Text('Sucursales'),
              onTap: () {
                // Actualiza el estado de la aplicación
 setState(() {
                  _currentWidget = Sucursales();
                });                // Luego cierra el drawer
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
      body: Container(
        margin: EdgeInsets.all(16.0), // Margen alrededor del borde
        decoration: BoxDecoration(
          border: Border.all(
            color: Colors.black, // Color del borde
            width: 2.0, // Ancho del borde
          ),
          borderRadius: BorderRadius.all(
            Radius.circular(12.0), // Radio de los bordes redondeados
          ),
        ),
        child: _currentWidget, // Muestra el widget actual dentro del borde
      ),
    );
  }
}