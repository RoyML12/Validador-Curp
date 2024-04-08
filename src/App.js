import React, { useState } from 'react';
import ReCAPTCHA from "react-google-recaptcha";
import './App.css';

function Modal({ isOpen, onClose, message }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <p>{message}</p>
        <button onClick={onClose}>Cerrar</button>
      </div>
    </div>
  );
}

function App() {

  const [nombre, setNombre] = useState('');
  const [primerApellido, setPrimerApellido] = useState('');
  const [segundoApellido, setSegundoApellido] = useState('');
  const [fechaNacimiento, setFechaNacimiento] = useState('');
  const [sexo, setSexo] = useState('');
  const [entidadNacimiento, setEntidadNacimiento] = useState('');
  const [captchaToken, setCaptchaToken] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMessage, setModalMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!captchaToken) {
      alert("Por favor, complete el captcha.");
      return;
    }

    const formData = {
      nombre,
      primer_apellido: primerApellido,
      segundo_apellido: segundoApellido,
      fecha_nac: fechaNacimiento,
      sexo: sexo === "hombre" ? "H" : "M",
      entidad: entidadNacimiento,
      captcha: captchaToken
    };

    const raw = JSON.stringify(formData);

    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: raw,
      redirect: "follow"
    };

    fetch("http://127.0.0.1:5000/curp", requestOptions)
      .then(response => response.text())
      .then(result => {
        setModalMessage(result);
        setIsModalOpen(true);
      })
      .catch(error => {
        setModalMessage(`Error: ${error.toString()}`);
        setIsModalOpen(true);
      });
  };


  const onChange = (token) => {
    setCaptchaToken(token); 
  };

  const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

 return (
  <>
  <h2 className="titulo">CURP</h2>
      <form onSubmit={handleSubmit} className="formulario">
        <label className="label">
          Nombre:
          <input type="text" value={nombre} onChange={e => setNombre(e.target.value)} className="input" />
        </label>
        <label className="label">
          Primer Apellido:
          <input type="text" value={primerApellido} onChange={e => setPrimerApellido(e.target.value)} className="input" />
        </label>
        <label className="label">
          Segundo Apellido:
          <input type="text" value={segundoApellido} onChange={e => setSegundoApellido(e.target.value)} className="input" />
        </label>
        <label className="label">
          Fecha de Nacimiento:
          <input type="text" value={fechaNacimiento} onChange={e => setFechaNacimiento(e.target.value)} className="input" />
        </label>
        <label className="label">
          Sexo:
          <select value={sexo} onChange={e => setSexo(e.target.value)} className="select">
            <option value="">Seleccione...</option>
            <option value="mujer">Mujer</option>
            <option value="hombre">Hombre</option>
          </select>
        </label>
        <label className="label">
          Entidad de Nacimiento:
          <input type="text" value={entidadNacimiento} onChange={e => setEntidadNacimiento(e.target.value)} className="input" />
        </label>
        <button type="submit" className="button">Enviar</button>
      </form>
      <div className="captcha-container">
        <ReCAPTCHA
          sitekey="6LfKE7QpAAAAALbV94lNY5FmJHhp2wDXosQ7k4Bn"
          onChange={onChange}
        />
      </div>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} message={modalMessage} />
</>
  );
}


export default App;
