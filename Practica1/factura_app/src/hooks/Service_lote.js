
import {GET,POST} from "./connection";

export async function lotes(token) {
    let datos =null;
     try {
        datos = await GET('lote');
     } catch (error) {   
        console.log(error.response.data);  
        return {"code":500}
     }
      return datos.data;
}
export async function save_lot(data,token) {
   let datos =null;
   console.log(data)
    try {
       datos = await POST('lote/guardarLote',data,token);
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
