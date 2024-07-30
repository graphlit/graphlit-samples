import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

const envSchema = z.object({
  GRAPHLIT_ENVIRONMENT_ID: z.string(),
  GRAPHLIT_ORGANIZATION_ID: z.string(),
  GRAPHLIT_JWT_SECRET: z.string(),
});

const env = envSchema.safeParse(process.env);

if (!env.success) {
  console.error('Invalid environment variables:', env.error.format());
  throw new Error('Invalid environment variables');
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    GRAPHLIT_ENVIRONMENT_ID: process.env.GRAPHLIT_ENVIRONMENT_ID,
    GRAPHLIT_ORGANIZATION_ID: process.env.GRAPHLIT_ORGANIZATION_ID,
    GRAPHLIT_JWT_SECRET: process.env.GRAPHLIT_JWT_SECRET,
  },
};

export default nextConfig;
