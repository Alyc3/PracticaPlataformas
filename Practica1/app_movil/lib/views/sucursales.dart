import 'package:app_movil/controllers/Service.dart';
import 'package:flutter/material.dart';

class Sucursales extends StatefulWidget {
  const Sucursales({Key? key}) : super(key: key);

  @override
  _SucursalesState createState() => _SucursalesState();
}

class _SucursalesState extends State<Sucursales> {
  List<Map<String, dynamic>> sucursales = [];
  String? selectedSucursal;
  List<DropdownMenuItem<String>> dropdownItems = [];
  List<Map<String, dynamic>> productos = [];

  @override
  void initState() {
    super.initState();
    cargarSucursal();
  }

  void cargarSucursal() async {
    try {
      Services service = Services();
      final value = await service.getSucursal();
      if (value.code == '200' && value.datos != null) {
        List<dynamic> sucursal = value.datos;
        setState(() {
          sucursales = sucursal
              .where((element) => element != null && element is Map<String, dynamic>)
              .map((element) {
            return {
              'nombre': element['nombre'],
              'external_id': element['external_id'],
              'latitud': element['latitud'],
              'longitud': element['longitud'],
            };
          }).toList();

          dropdownItems = sucursales.map((sucursal) {
            return DropdownMenuItem<String>(
              value: sucursal['external_id'].toString(),
              child: Text(sucursal['nombre']),
            );
          }).toList();
        });
      }
    } catch (e) {
      print("Error al cargar la persona: $e");
    }
  }

  void cargarProductosSucursal(String externalId) async {
    try {
      Services service = Services();
      final value = await service.getProducto(externalId);
      if (value.code == '200' && value.datos != null) {
        List<dynamic> productosData = value.datos;
        setState(() {
          productos = productosData
              .where((element) => element != null && element is Map<String, dynamic>)
              .map((element) {
            return {
              'descripcion': element['descripcion'],
              'precio': element['precio'],
              'nombre': element['nombre'],
              'stock': element['stock'],
            };
          }).toList();
        });
      }
    } catch (e) {
      print("Error al cargar los productos de la sucursal: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sucursales'),
      ),
      body: Column(
        children: [
          DropdownButton<String>(
            hint: Text('Seleccione una sucursal'),
            value: selectedSucursal,
            items: dropdownItems,
            onChanged: (String? newValue) {
              setState(() {
                selectedSucursal = newValue;
                if (newValue != null) {
                  cargarProductosSucursal(newValue);
                }
              });
            },
          ),
          Expanded(
            child: ListView.builder(
              itemCount: productos.length,
              itemBuilder: (context, index) {
                final producto = productos[index];
                return Card(
                  child: ListTile(
                    title: Text(producto['nombre']),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Descripción: ${producto['descripcion']}'),
                        Text('Precio: ${producto['precio']}'),
                        Text('Stock: ${producto['stock']}'),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}