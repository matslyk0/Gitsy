import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import Report from "../../components/Report/Report.jsx";
import styles from "./CreateReport.module.css";
import loadingWheel from "../../assets/bars.svg";
import processReport from "../../assets/process-svgrepo-com.svg";
import axios from "axios";
import { useState } from "react";
import { Toaster, toast } from "sonner";

function ReportForm({ url, setUrl, onAnalyse, disabled }) {
  return (
    <div className={styles.reportForm}>
      <input
        disabled={disabled}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter a GitHub Repo URL"
        type="text"
        value={url}
      />
      <button onClick={onAnalyse}>
        <img src={processReport} />
      </button>
    </div>
  );
}

export default function CreateReport() {
  const [url, setUrl] = useState("");
  const [reportData, setReportData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [ownerAndName, setOwnerAndName] = useState("owner/name");

  async function onAnalyse() {
    if (!url) return;

    setUrl("");
    setIsLoading(true);
    setOwnerAndName(url.replace("https://github.com/", ""));

    const params = { repo_url: url };
    const apiUrl =
      import.meta.env.MODE === "development"
        ? "http://localhost:8000/create-report/generate"
        : "/api/create-report/generate";

    try {
      const response = await axios.get(apiUrl, { params: params });
      setReportData(response.data);
    } catch (error) {
      if (error.response && error.response.status == 404) {
        toast.error("The entered URL is invalid.");
      } else if (error.request) {
        toast.error("Check your connection.");
      } else {
        console.error("Unknown Error", error.message);
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <Banner />
      <main className={styles.mainContent}>
        {!reportData && (
          <h1 className={styles.createReportHeader}>Create a Report Here</h1>
        )}

        {reportData ? (
          <>
            <Report reportData={reportData} ownerAndName={ownerAndName} />
            <button onClick={() => setReportData(null)}>Create Another</button>
          </>
        ) : (
          <>
            <ReportForm
              url={url}
              setUrl={setUrl}
              onAnalyse={onAnalyse}
              disabled={isLoading}
            />
            <div className={styles.loadingWheelDiv}>
              {isLoading && <img src={loadingWheel} />}
            </div>
          </>
        )}
      </main>
      <Footer />
      <Toaster
        toastOptions={{
          style: {
            backgroundColor: "rgb(60, 60, 100)",
            border: "0px",
            color: "white",
            maxWidth: "225px",
          },
        }}
      />
    </>
  );
}
