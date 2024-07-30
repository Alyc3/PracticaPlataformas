import 'package:app_movil/models/ResponseGeneric.dart';

class Session extends ResponseGeneric{
  String external_id = "";
  String token = "";
  String user = "";
  void add(ResponseGeneric rg){
    code = rg.msg;
    msg = rg.msg;
    datos = rg.datos;
  }
}