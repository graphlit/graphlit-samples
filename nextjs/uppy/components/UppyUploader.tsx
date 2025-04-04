"use client";

import { useEffect, useState } from "react";
import Uppy from "@uppy/core";
import { Dashboard } from "@uppy/react";
import Tus from "@uppy/tus";
// Configure desired Companion plugins
// https://uppy.io/docs/dropbox/
import Dropbox from '@uppy/dropbox';
// https://uppy.io/docs/google-drive-picker/
import GoogleDrivePicker from '@uppy/google-drive-picker';
import "@uppy/core/dist/style.css";
import "@uppy/dashboard/dist/style.css";

export default function UppyUploader() {
  const [uppy, setUppy] = useState<Uppy | null>(null);
  const [status, setStatus] = useState("Idle");

  useEffect(() => {
    async function setupUppy() {
      try {
        setStatus("Fetching JWT...");
        const response = await fetch("/api/auth");
        const { token } = await response.json();

        setStatus("Fetched JWT");

        const newUppy = new Uppy({ 
            autoProceed: false
          })
          .use(Dropbox, {
            companionUrl: "https://companion.graphlit.io"
          })
          .use(GoogleDrivePicker, {
            companionUrl: "https://companion.graphlit.io",
            clientId: process.env.NEXT_PUBLIC_GOOGLE_DRIVE_CLIENT_ID || "",
            appId: process.env.NEXT_PUBLIC_GOOGLE_DRIVE_APP_ID || "",
            apiKey: process.env.NEXT_PUBLIC_GOOGLE_DRIVE_API_KEY || ""
          })
          .use(Tus, {
            endpoint: "https://tus-scus.graphlit.io/api/v1/tus",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
        
        newUppy.on("file-added", (file) => {
          if (file.size)
            setStatus(`Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);

          //newUppy.setFileMeta(file.id, {
          //  workflowId: "TODO",
          //});
        });

        newUppy.on("upload-progress", (file, progress) => {
          if (progress.bytesTotal)
            setStatus(`Uploading: ${Math.round((progress.bytesUploaded / progress.bytesTotal) * 100)}%`);
        });

        newUppy.on("upload-success", (file, response) => {
          setStatus("Upload successful!");
        });

        newUppy.on("error", () => setStatus("Upload failed."));

        setUppy(newUppy);
      } catch (error) {
        setStatus("Failed to get JWT");
        console.error("Failed to get JWT", error);
      }
    }

    setupUppy();
    return () => uppy?.destroy();
  }, []);

  return (
    <div className="w-full max-w-lg text-center">
      <p className="mb-2 font-medium">Status: {status}</p>      
      {uppy ? <Dashboard uppy={uppy} plugins={["Companion"]} /> : null}
    </div>
  );
}