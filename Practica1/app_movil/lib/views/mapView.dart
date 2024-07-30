import 'dart:async';

import 'package:app_movil/controllers/Service.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class MapView extends StatefulWidget {
  const MapView({super.key});

  @override
  MapViewState createState() => MapViewState();
}

class MapViewState extends State<MapView> {
  LatLng markerPosition = LatLng(-1.831239, -78.183406); // Posición inicial del marcador
  List<Map<String, dynamic>> sucursales = [];
  List<Marker> markers = [];
  List<Map<String, dynamic>> productosVencidos = [];
  String selectedSucursal = '';

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
          _addMarkers();
        });
      }
    } catch (e) {
      print("Error al cargar la persona: $e");
    }
  }

  void obtenerProductosVencidos(String external_id) async {
    try {
      Services service = Services();
      final value = await service.getPrVencidos(external_id);
      print(value.datos);
      if (value.code == '200' && value.datos != null) {
        List<dynamic> productos = value.datos;
        setState(() {
          productosVencidos = productos
              .where((element) => element != null && element is Map<String, dynamic>)
              .map((element) {
            return {
              'external_id': element['external_id'],
              'descripcion': element['descripcion'],
              'precio': element['precio'],
            };
          }).toList();
          selectedSucursal = external_id;
        });
      }
    } catch (e) {
      print("Error al cargar los productos: $e");
    }
  }

  void _addMarkers() {
    markers = sucursales.map((sucursal) {
      return Marker(
        width: 80.0,
        height: 80.0,
        point: LatLng(sucursal['latitud'], sucursal['longitud']),
        child:  GestureDetector(
          onTap: () {
            obtenerProductosVencidos(sucursal['external_id']);
          },
          child: Icon(
            Icons.location_on,
            color: Color.fromARGB(255, 60, 189, 214),
            size: 40,
          ),
        ),
      );
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          FlutterMap(
            options: MapOptions(
              initialCenter: markerPosition,
              initialZoom: 9.2,
              onTap: (tapPosition, point) {
                setState(() {
                  markerPosition = point;
                });
              },
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.app',
              ),
              RichAttributionWidget(
                attributions: [
                  TextSourceAttribution(
                    'OpenStreetMap contributors',
                    onTap: () => Uri.parse('https://openstreetmap.org/copyright'),
                  ),
                ],
              ),
              MarkerLayer(
                markers: markers,
              ),
            ],
          ),
          if (productosVencidos.isNotEmpty)
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                padding: EdgeInsets.all(10),
                margin: EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Productos Vencidos',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    ...productosVencidos.map((producto) {
                      return ListTile(
                        title: Text(producto['descripcion']),
                        subtitle: Text('Precio: ${producto['precio']}'),
                      );
                    }).toList(),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}