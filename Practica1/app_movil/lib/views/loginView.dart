//fstful
import 'dart:developer';
import 'package:app_movil/controllers/Service.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:validators/validators.dart';
class LoginView extends StatefulWidget {
  const LoginView({ Key? key }) : super(key: key);

  @override
  _LoginViewState createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController correoController = TextEditingController();
  final TextEditingController claveController = TextEditingController();
  void inicio(){
    FToast fToast = FToast();
    fToast.init(context);
    setState(() {
      if(_formKey.currentState!.validate()){
        Map<String, String> data = {
          "correo": correoController.text,
          "clave": claveController.text
        };
        log(data.toString());
        Services c = Services();
        c.session(data).then((value)async{
          log(value.toString());
          if (value.code == 'OK'){
            fToast.showToast(
              child: Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.green,
                  borderRadius: BorderRadius.circular(25),
                ),
                child: const Text("Inicio de sesion exitoso",
                style: TextStyle(
                  color: Colors.white
                ))
              ),
              gravity: ToastGravity.BOTTOM,
              toastDuration: const Duration(seconds: 2),
            );
            await Future.delayed(const Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/Dashboard');
            });
         log(value.msg);
         log(value.token);
         

        }else {
          log(value.code.toString());
          fToast.showToast(
            child: Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(25),
              ),
              child: const Text("Inicio de sesion fallido",
              style: TextStyle(
                color: Colors.white
              ))
            ),
            gravity: ToastGravity.BOTTOM,
            toastDuration: const Duration(seconds: 2),
          );
        }
        }
        );
      
      }
    
    });
  }
  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Scaffold(
        body: ListView(
          padding: const EdgeInsets.all(32),
          children: <Widget>[
            Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.all(10),
              child: const Text("Censo",
              style: TextStyle(
                color: Colors.blue,
                fontWeight: FontWeight.bold,
                fontSize: 30
              ))
            ),
            Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.all(10),
              child: const Text("La mejor app de noticias",
              style: TextStyle(                
                fontSize: 20
              ))
            ),
            Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.all(10),
              child: const Text("Inicio de sesion",
              style: TextStyle(                
                fontSize: 20,
                fontWeight: FontWeight.bold
              ))
            ),
            Container(
              padding: const EdgeInsets.all(10),
              child: TextFormField(
                
                decoration: const InputDecoration(
                  labelText: 'Correo',
                  suffixIcon: Icon(Icons.alternate_email)),
                  validator:(value){
                  if(value!.isEmpty){
                    return "Por favor ingrese un correo";
                  }
                  if(!isEmail(value)){
                    return "Por favor ingrese un correo valido";
                  }
                },
                controller: correoController,
              ),
            ),
            Container(
              padding: const EdgeInsets.all(10),
              
              child: TextFormField(
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Clave',
                  suffixIcon: Icon(Icons.key)),
                validator:(value){
                if(value!.isEmpty){
                   return "Por favor ingrese un clave";
                }
                
                },
                
              controller: claveController,
              ),
            ),
            Container(
              height: 50,
              padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
              child: ElevatedButton(
                onPressed: inicio,
                child: const Text("Inicio")
              ),
            ),
            Row(
              children: <Widget>[
                const Text('No tienes una cuenta!'),
                TextButton(
                  onPressed: (){
                    Navigator.pushNamed(context, '/register');
                  }, 
                  child: const Text(
                    'Registrate',
                    style: TextStyle(fontSize: 20),
                  ))
              ],
            )
          ],
        ),
      ),
    );
  }
}