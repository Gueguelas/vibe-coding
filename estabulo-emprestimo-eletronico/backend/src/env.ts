import { z } from "zod";

// Variáveis de ambiente validadas com Zod no boot (ADR-001, seção 9).
const envSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.string().min(1, "DATABASE_URL é obrigatória"),
  DIRECT_URL: z.string().min(1, "DIRECT_URL é obrigatória"),
  SUPABASE_URL: z.string().url("SUPABASE_URL deve ser uma URL válida")
});

export type Env = z.infer<typeof envSchema>;

export const ENV = "ENV";

export function carregarEnv(fonte: NodeJS.ProcessEnv = process.env): Env {
  const resultado = envSchema.safeParse(fonte);
  if (!resultado.success) {
    const detalhes = resultado.error.issues
      .map((i) => `${i.path.join(".")}: ${i.message}`)
      .join("; ");
    throw new Error(`Variáveis de ambiente inválidas — ${detalhes}`);
  }
  return resultado.data;
}

// Módulo global: qualquer módulo (Prisma, guards, services) injeta ENV
// sem precisar importar cadeias de módulos — env validado uma vez no boot.
import { Global, Module } from "@nestjs/common";

@Global()
@Module({
  providers: [{ provide: ENV, useFactory: () => carregarEnv() }],
  exports: [ENV]
})
export class EnvModule {}
