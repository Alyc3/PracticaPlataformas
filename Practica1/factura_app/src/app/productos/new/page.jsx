'use client';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { set, useForm } from 'react-hook-form';
import { POST } from '@/hooks/connection.js';
import swal from 'sweetalert';
import Cookies from 'js-cookie';
//import localStorage from 'local-storage';
import { lotes } from '@/hooks/Service_lote';
import { useRouter } from 'next/navigation';
import { guardaProducto } from '@/hooks/Service_producto';

import { useState, useEffect } from 'react';

export default function New() {
    const router = useRouter();
    const [externalId, setExternalId] = useState('');
    const [lotesList, setLotesList] = useState(null);
    let token = Cookies.get('token');
    

    /* useEffect(() => {
        const id = localStorage.getItem('external_id');
        setExternalId(id);
        console.log(id);
    }, []); */
    useEffect(() => {
    
        if (!lotesList) {
            lotes(token).then((info) => {
                if (info.code == '200') {
                    setLotesList(info.datos);
                    console.log(info.datos);
                } else {
                    setLotesList([]);
                }
            });
        }
    }, [ lotesList]);

    const validationSchema = Yup.object().shape({
        nombre: Yup.string().trim().required('El nombre del producto es necesario'),
        descripcion: Yup.string().required('Descripcion del producto'),
        precio: Yup.number().required('Precio del producto'),
        stock: Yup.number().required('Stock de producto'),

    });
    const formOptions = { resolver: yupResolver(validationSchema) };
    const { register, handleSubmit, formState } = useForm(formOptions);
    let { errors } = formState;
    
    const sendInfo = async (data) => {
        
        console.log(data);
        const dataToSend = {
            nombre: data.nombre,
            descripcion: data.descripcion,
            precio: data.precio,
            stock: data.stock

        };
        const info = await guardaProducto(dataToSend, token);
        console.log(info.dataToSend);
        if (info && info.code == 200) {
            swal({
                title: "Registro de producto",
                text: "Producto registrado correctamente",
                icon: "success",
                button: "Aceptar",
                timer: 4000,
                closeOnEsc: true,
            });
            router.push('/producto');
        } else {
            swal({
                title: "Error",
                text: info && info.datos ? info.datos.error : "Error desconocido",
                icon: "error",
                button: "Aceptar",
                timer: 4000,
                closeOnEsc: true,
            });
        }
    };
    
    return (
        <div className="container text-center mt-5" style={{ width: "40%", border: "2px solid white", background: "white", padding: "20px", borderRadius: "15px", margin: "auto" }}> 
            <form onSubmit={handleSubmit(sendInfo)} className="form-signin">
            <div className="mb-3">
                        <label className="form-label">Lote:</label>
                        <select {...register('lote')} name="lote" className="form-control">
                            <option value="">Selecciona un lote...</option>
                            {lotesList && lotesList.map((lote, index) => (
                                <option key={index} value={lote.external_id}>{lote.nombre}</option>
                            ))}
                        </select>
                        {errors.lote && <div>{errors.lote?.message}</div>}
            </div>

                <div className="mb-3">
                    <label className="form-label">Nombre de Producto:</label>
                    <input type="text" {...register('nombre')} name="nombre" placeholder="Nombre de producto" className="form-control"/>
                    {errors.nombre && <div>{errors.nombre?.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Descripcion:</label>
                    <input type="text" {...register('descripcion')} name="descripcion" placeholder="Descripcion del producto" className="form-control"/>
                    {errors.descripcion && <div>{errors.descripcion?.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Precio:</label>
                    <input type="text" {...register('precio')} name="precio" placeholder="Precio del productos" className="form-control"/>
                    {errors.precio && <div>{errors.precio?.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Stock de producto:</label>
                    <input type="text" {...register('stock')} name="stock" placeholder="Stock del productos" className="form-control"/>
                    {errors.stock && <div>{errors.stock?.message}</div>}
                </div>
                
                <button type="submit" className="w-100 btn btn-sm btn-primary">Registrar Producto</button>
            </form>
        </div>
    );
}