'use client';
import "bootstrap/dist/css/bootstrap.min.css";
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { set, useForm } from 'react-hook-form';
import swal from 'sweetalert';
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';
import { useEffect, useState ,useRef} from 'react';
import { buscar_lote, update_lote ,editar_Imagen} from '@/hooks/Service_lote';

export default function Editar(params) {
    const router = useRouter();
    let token = Cookies.get('token');
    let [lote, setLote] = useState(null);
    const fileInputRef = useRef(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState(lote ? lote.imagen : '');
    const [selectedFile, setSelectedFile] = useState(null);


    useEffect(() => {
        if (params.params) {
            buscar_lote (token, params.params).then((info) => {
                if (info.code == '200') {
                    setLote(info.datos);
                    console.log(info.datos);
                }
            });
        }
    }, [params.params, token]);

    useEffect(() => {
        if (selectedFile) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreviewUrl(reader.result);
            };
            reader.readAsDataURL(selectedFile);
        } else if (lote && lote.imagen) {
            setImagePreviewUrl(lote.imagen);
        }
    }, [selectedFile, lote]);

    const validationSchema = Yup.object().shape({
        nombrePr: Yup.string().trim().required('El nombre del producto es requerido'),
        fechaPr: Yup.date().required('La fecha de producción es requerida'),
        fechaVen: Yup.date().required('La fecha de vencimiento es requerida'),
        imagen : Yup.string().required('La imagen es requerida'),
        cantidadL: Yup.number().required('La cantidad es requerida')
    });

    const formOptions = { resolver: yupResolver(validationSchema) };
    const { register, handleSubmit, formState: { errors }, setValue } = useForm(formOptions);

    useEffect(() => {
        if (lote) {
            setValue('nombrePr', lote.nombrePr);
            setValue('fechaPr', lote.fechaPr);
            setValue('fechaVen', lote.fechaVen);
            setValue('cantidadL', lote.cantidadL);
            setValue('imagen', lote.imagen);
        }
    }, [lote, setValue]);
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
    
        const token = Cookies.get('token'); // Asegúrate de obtener el token como lo haces en otros lugares de tu código
        const formData = new FormData();
        formData.append('imagen', selectedFile);
        // Ajusta la función editar_Imagen para que acepte formData como parámetro
        const resultado = await editar_Imagen(formData, token);
        // Maneja el resultado como sea necesario
        console.log(resultado);
      };
    const sendInfo = async (data) => {
        const info = await update_lote(data, params.params, token);
        console.log(info);
        if (info && info.status == '200') {
            swal("Registro exitoso", "Lote actualizado correctamente", "success");
            router.push('/lote');
        } else {
            swal("Error", info ? info.datos.error : "Error desconocido", "error");
        }
    };

    return (
        <div className="container text-center mt-5" style={{ width: "40%", border: "2px solid black", padding: "20px", borderRadius: "15px", margin: "auto" }}>
            <form onSubmit={handleSubmit(sendInfo)} className="form-signin">
                {/* Form fields for lote data */}
                <div className="mb-3">
                    <label className="form-label">Nombre del Producto:</label>
                    <input type="text" {...register('nombrePr')} placeholder="Nombre del Producto" className="form-control"/>
                    {errors.nombrePr && <div>{errors.nombrePr.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Fecha de Produccion:</label>
                    <input type="Date" {...register('fechaPr')} placeholder="Fecha de Produccion" className="form-control"/>
                    {errors.fechaPr && <div>{errors.fechaPr.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Fecha de Vencimiento:</label>
                    <input type="Date" {...register('fechaVen')} placeholder="Fecha de Vencimiento" className="form-control"/>
                    {errors.fechaVen && <div>{errors.fechaVen.message}</div>}
                </div>
                <div className="mb-3">
                    <label className="form-label">Cantidad:</label>
                    <input type="number" {...register('cantidadL')} className="form-control"/>
                    {errors.cantidadL && <div>{errors.cantidadL.message}</div>}
                </div>
                <div>
                <button className="btn btn-primary" onClick={handleSelectImage}>Seleccionar Imagen</button>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                    accept="image/*"
                />
                <button className="btn btn-secondary" onClick={handleEditarImagen}>Editar Imagen</button>
            </div>
            {imagePreviewUrl && (
                <div className="image-preview" style={{ marginTop: '20px' }}>
                    <img src={imagePreviewUrl} alt="Vista previa de la imagen" style={{ maxWidth: '100%', height: 'auto' }} />
                </div>
            )}
                
                <button type="submit" className="w-100 btn btn-sm btn-primary">Actualizar Lote</button>
            </form>
        </div>
    );
}