import 'dart:convert';
import 'package:app_movil/models/ResponseGeneric.dart';
import 'package:http/http.dart' as http;

class Connection {
  final String urlBase = "http://192.168.1.6:5000/";
  static const String URL_MEDIA = "http://192.168.1.6:5000/media";

  Future<ResponseGeneric> get(String resource, {String token = "NONE"}) async {
      final String url = urlBase + resource;
      Map<String, String> headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
      };
  
      
      if (token != "NONE") {
        headers['X-Access-Token'] = token;
      }
  
      final uri = Uri.parse(url);
      final response = await http.get(uri, headers: headers);
  
      if (response.statusCode == 200) {
        Map<dynamic, dynamic> body = jsonDecode(response.body);
        print(body);
        return _response(body['code'].toString(), body['msg'], body['datos']);
      } else {
        throw Exception('Failed to load data');
      }
    }

  ResponseGeneric _response(String code, String msg, dynamic datos) {
    var response = ResponseGeneric();
    response.msg = msg;
    response.code = code;
    response.datos = datos;
    return response;
  }

  Future<ResponseGeneric> post(
      String resource, Map<dynamic, dynamic> data, { token = "NONE"}) async {
    final String url = urlBase + resource;
    Map<String, String> headers = {
      'Accept': "application/json",
      'Content-Type': "application/json"
    };

    // Verifica si se proporcionó un token y no es "NONE", luego lo agrega a los headers
    if (token != "NONE") {
      headers['X-Access-Token'] = token;
    }

    final uri = Uri.parse(url);
    final response = await http.post(uri, headers: headers, body: jsonEncode(data));

    if (response.statusCode == 200) {
      // Verifica si el cuerpo de la respuesta es null o no contiene los campos esperados
      final body = jsonDecode(response.body);
      if (body == null ||
          !body.containsKey('code') ||
          !body.containsKey('msg') ||
          !body.containsKey('datos')) {
        throw Exception('Respuesta inesperada del servidor');
      }
      Map<String, dynamic> datos =
          body['datos'] != null ? Map<String, dynamic>.from(body['datos'] as Map<dynamic, dynamic>) : {};
      return _response(body['code'].toString(), body['msg'], datos);
    } else {
      throw Exception('Failed to post data');
    }
  }
}