
import {GET,POST} from "./connection";

export async function productos() {
    let datos =null;
     try {
        datos = await GET('producto');
     } catch (error) {   
        console.log(error.response.data);  
        return {"code":500}
     }
      return datos.data;
}
export async function guardaProducto(data) {
   let datos =null;
   console.log(data)
    try {
       datos = await POST('/producto/guardarProducto/0361c0da-dd88-4343-be5f-25be6e965299',data,token);
       console.log(data)
    } catch (error) {   
       console.log(error.response.data);  
       return {"code":500}
    }
     return datos.data;
}
export async function  buscar_lote(token,params){
   let datos = null;
   try {
   
      datos = await GET('lote/'+params.external);
   } catch (error) {
      console.log(error.response.data);
      return{"code": 500}
   }
   return datos.data;
}


export async function update_lote(data,params, token) {
   try {
       return await POST('lote/'+params.external, data, token);
   } catch (error) {
       console.error(error);
       return null;
   }
}    

export async function subirImagen(data,token){
   try {
       return await POST('/lote/subir_imagen_lote/<external_id>', data, token);
   } catch (error) {
       console.error(error);
       return null;
   }
}

export async function editar_Imagen(params,token){
let datos = null;
console.log(params)
try {
   datos = await POST('/lote/subir_imagen_lote/'+params.get('external_id'),params,token);
}
catch (error) {
   console.log(error.response.data);
   return{"code": 500}
}
return datos.data;
// TODO agarrar errores
}
