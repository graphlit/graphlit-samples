"use client";

import { useEffect, useState } from "react";
import Uppy from "@uppy/core";
import { Dashboard } from "@uppy/react";
import Tus from "@uppy/tus";
import { COMPANION_URL, COMPANION_ALLOWED_HOSTS } from '@uppy/transloadit';
import Dropbox from '@uppy/dropbox';
import GoogleDrive from '@uppy/google-drive';
import "@uppy/core/dist/style.css";
import "@uppy/dashboard/dist/style.css";

export default function UppyUploader() {
  const [uppy, setUppy] = useState<Uppy | null>(null);
  const [status, setStatus] = useState("Idle");
  const [fileUrl, setFileUrl] = useState<string | null>(null);

  useEffect(() => {
    async function setupUppy() {
      try {
        setStatus("Fetching JWT...");
        const response = await fetch("/api/auth");
        const { token } = await response.json();

        const newUppy = new Uppy({ autoProceed: false })
          .use(Dropbox, {
            companionUrl: COMPANION_URL,
            companionAllowedHosts: COMPANION_ALLOWED_HOSTS,
          })
          .use(GoogleDrive, {
            companionUrl: COMPANION_URL,
            companionAllowedHosts: COMPANION_ALLOWED_HOSTS,
          })
          .use(Tus, {
            endpoint: "https://tus-scus-dev.graphlit.io/api/v1/tus",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

        newUppy.on("file-added", (file) => {
          if (file.size)
            setStatus(`Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
        });

        newUppy.on("upload-progress", (file, progress) => {
          if (progress.bytesTotal)
            setStatus(`Uploading: ${Math.round((progress.bytesUploaded / progress.bytesTotal) * 100)}%`);
        });

        newUppy.on("upload-success", (file, response) => {
          setStatus("Upload successful!");
          if (response.uploadURL)
            setFileUrl(response.uploadURL);
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
      {fileUrl && (
        <p className="mt-2 text-green-600">
          <a href={fileUrl} target="_blank" rel="noopener noreferrer" className="underline">Download File</a>
        </p>
      )}
      {uppy ? <Dashboard uppy={uppy} plugins={["Companion"]} /> : null}
    </div>
  );
}