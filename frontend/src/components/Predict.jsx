import { useState } from "react";
import axios from "axios";

export default function Predict() {
  const [purchase, setPurchase] = useState(0);
  const [calls, setCalls] = useState(0);
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/predict`, [
      { purchase_amount: parseFloat(purchase), support_calls: parseInt(calls) },
    ]);
    setResult(res.data);
  };

  return (
    <div class="container mt-4">
      <h2 class="mb-3">Predict</h2>
      <div class="row g-3">
        <div class="col-md-6">
          <input
            type="number"
            class="form-control"
            value={purchase}
            onChange={(e) => setPurchase(e.target.value)}
            placeholder="Purchase Amount"
          />
        </div>
        <div class="col-md-6">
          <input
            type="number"
            class="form-control"
            value={calls}
            onChange={(e) => setCalls(e.target.value)}
            placeholder="Support Calls"
          />
        </div>
        <div class="col-12">
          <button class="btn btn-primary" onClick={handlePredict}>
            Predict
          </button>
        </div>
      </div>
      {result && (
        <div class="mt-3">
          <p class="fw-bold">Prediction: {result?.prediction ?? "N/A"}</p>
          <p class="fw-bold">Probability: {result?.probability?.[0] ?? "N/A"}</p>
        </div>
      )}
    </div>
  );
}
