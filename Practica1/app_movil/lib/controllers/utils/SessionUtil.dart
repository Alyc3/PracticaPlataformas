// ignore: file_names

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
class SessionUtil {
  final storage = new FlutterSecureStorage();
  void add(key,value)async {
    await storage.write(key:key,value:value);
    
  }
  void removeItemte(key,value)async {
    await storage.write(key:key,value:value);
    
  }
  void removeAll(key,value)async {
    await storage.write(key:key,value:value);
    
  }
  Future<String?> getValue(key) async {
    return storage.read(key:key);
  }
}