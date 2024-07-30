import 'package:app_movil/controllers/Connection.dart';
import 'package:app_movil/models/ResponseGeneric.dart';
import 'package:app_movil/models/Session.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';


class Services {
  final Connection _con = Connection();
  String getMedia(){
    return Connection.URL_MEDIA;
  }
  final FlutterSecureStorage finSec = const FlutterSecureStorage();
  Future <Session> session(Map<dynamic,dynamic> map) async {
      ResponseGeneric rg = await _con.post("sesion", map);
        Session s = Session();
        s.add(rg);
      if(rg.code == '200'){
        s.external_id = rg.datos['external_id'];
        s.token = rg.datos['token'];
        s.user = rg.datos['user'];
        await finSec.write(key : 'external_id', value : s.external_id);
        await finSec.write(key : 'token', value : s.token);
        await finSec.write(key : 'user', value : s.user);
        
      }
      return s;
  }
  Future<ResponseGeneric> guardarPersona(
    String external_id, Map<dynamic, dynamic> map) async {
    String? token = await getToken();
    return _con.post("modificar_cuenta/$external_id", map, token: token);
  }

  Future <ResponseGeneric> getSucursales() async {
    return await _con.get("sucursal");
  }
  Future<String?> getExternalP() async {
    return await finSec.read(key: 'external_id');
  }
  Future<String?> getToken() async {
    return await finSec.read(key: 'token');
  }
  Future <ResponseGeneric> getPersona() async {
    String? external_id = await getExternalP();
    return await _con.get("persona/$external_id");
  }

  Future <ResponseGeneric> getSucursal() async {
    return await _con.get("sucursal");
  }

  Future<ResponseGeneric> getPrVencidos(String external_id) async {
    return await _con.get("/estado_producto/$external_id");
  }

  Future<ResponseGeneric> getProducto(String external_id) async {
    return await _con.get("/lote/sucursal/$external_id");
  }


}
