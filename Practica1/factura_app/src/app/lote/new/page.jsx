'use client';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useForm } from 'react-hook-form';
import { POST } from '@/hooks/connection.js';
import swal from 'sweetalert';
import Cookies from 'js-cookie';
import { save_lot } from '@/hooks/Service_lote'; // Asegúrate de que esta importación sea correcta
import { useRouter } from 'next/navigation';
//import React, { useRef, useState } from 'react';
import { useState, useEffect,useRef } from 'react';

export default function New() {
    const [selectedFile, setSelectedFile] = useState(null);
    const fileInputRef = useRef(null);
    const router = useRouter();
    let token = Cookies.get('token');

    const handleSelectImage = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    const handleEditarImagen = async () => {
        if (!selectedFile) {
            console.log("No se ha seleccionado ningún archivo.");
            return;
        }
    const formData = new FormData();
        formData.append('imagen', selectedFile);

        // Asegúrate de implementar la función editar_Imagen para que acepte formData y token como parámetros
    const resultado = await editar_Imagen(formData, token);
        console.log(resultado);
    };

    const validationSchema = Yup.object().shape({
        nombrePr: Yup.string().trim().required('El  del lote es requerido'),
        fechaPr: Yup.date().required('La fecha de produccion es requerida'),
        fechaVen: Yup.date().required('La fecha de vencimiento es requerida'),
        cantidadL: Yup.number().required('La cantidad es requerida'),

    });
    const formOptions = { resolver: yupResolver(validationSchema) };
    const { register, handleSubmit, formState } = useForm(formOptions);
    let { errors } = formState;
    
    const sendInfo = async (data) => {
        const formatDate = (date) => {
            let newDate = new Date(date);
            let year = newDate.getFullYear();
            let month = ('0' + (newDate.getMonth() + 1)).slice(-2);
            let day = ('0' + newDate.getDate()).slice(-2);
            return `${day}/${month}/${year}`;
        };
        console.log(data);
        const dataToSend = {
            nombrePr: data.nombrePr,
            fechaPr: formatDate(data.fechaPr),
            fechaVen: formatDate(data.fechaVen),
            cantidadL: data.cantidadL,
        };
        const info = await save_lot(dataToSend, token);
        console.log(info.dataToSend);
        if (info && info.code == 200) {
            swal({
                title: "Registro exitoso",
                text: "Lote registrado correctamente",
                icon: "success",
                button: "Aceptar",
                timer: 4000,
                closeOnEsc: true,
            });
            router.push('/lote');
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
                    <label className="form-label">Nombre del Lote:</label>
                    <input type="text" {...register('nombrePr')} name="nombrePr" placeholder="Nombre del Lote" className="form-control"/>
                    {errors.nombrePr && <div>{errors.nombrePr?.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Fecha de Produccion:</label>
                    <input type="date" name="fechaPr" {...register('fechaPr')} className="form-control"/>
                    {errors.fechaPr && <div>{errors.fechaPr?.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Fecha de Vencimiento:</label>
                    <input type="date" name="fechaVen" {...register('fechaVen')} className="form-control"/>
                    {errors.fechaVen && <div>{errors.fechaVen?.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Cantidad:</label>
                    <input type="text" {...register('cantidadL')} name="cantidadL" placeholder="Cantidad de productos" className="form-control"/>
                    {errors.cantidadL && <div>{errors.cantidadL?.message}</div>}
                </div>
                <div className="container text-center mt-5">
                    <input
                    type="file"
                    style={{ display: 'none' }}
                    ref={fileInputRef}
                    onChange={handleFileChange}
                />
                <button onClick={handleSelectImage}>Subir Imagen</button>
                <button onClick={handleEditarImagen}>Guardar Imagen</button>
                {/* Agrega aquí más elementos de la UI según sea necesario */}
                </div>
                <button type="submit" className="w-100 btn btn-sm btn-primary">Registrar Lote</button>
            </form>
        </div>
    );
}