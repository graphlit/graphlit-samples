import UppyUploader from "../components/UppyUploader";
import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-gray-100">
      <div className="absolute top-4 left-4">
        <Image src="/graphlit-logo.svg" alt="Logo" width={120} height={60} className="rounded-lg shadow-md" />
      </div>
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Next.js + Uppy + Tus</h1>
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <UppyUploader />
      </div>
    </main>
  );
}