import { useState } from "react";
import axios from "axios";

export default function Retrain() {
 const [file, setFile] = useState(null);
   const [message, setMessage] = useState("");
 
   const handleUpload = async () => {
     if (!file) return alert("Please select a CSV file");
     const formData = new FormData();
     formData.append("file", file);
     const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/retrain`, formData);
     setMessage(res.data.message);
   };
 
  return (
    <div className="container mt-4">
      <h2 className="mb-3">Retrain Model</h2>
      <div className="row g-3">
        <div className="col-12">
            <input 
            className="form-control-file" 
            type="file" accept=".csv" 
            onChange={e => setFile(e.target.files[0])} 
            />
         
        </div>
        <div className="col-12">
          <button className="btn btn-primary" onClick={handleUpload}>
            Train
          </button>
        </div>
      </div>
      <p className="mt-3">{message}</p>
    </div>
  )
}
