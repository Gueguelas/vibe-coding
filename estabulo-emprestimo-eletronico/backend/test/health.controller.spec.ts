import { INestApplication } from "@nestjs/common";
import { APP_FILTER, APP_GUARD } from "@nestjs/core";
import { Test } from "@nestjs/testing";
import request from "supertest";
import { JwtGuard } from "../src/auth/jwt.guard";
import { ProblemDetailsFilter } from "../src/erros/problem-details.filter";
import { ENV } from "../src/env";
import { HealthModule } from "../src/health/health.module";

const envTeste = {
  NODE_ENV: "test" as const,
  PORT: 3000,
  DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/stable",
  DIRECT_URL: "postgresql://postgres:postgres@localhost:5432/stable",
  SUPABASE_URL: "http://localhost:54321"
};

describe("GET /health", () => {
  let app: INestApplication;

  beforeAll(async () => {
    const modulo = await Test.createTestingModule({
      imports: [HealthModule],
      providers: [
        { provide: ENV, useValue: envTeste },
        JwtGuard,
        { provide: APP_GUARD, useExisting: JwtGuard },
        { provide: APP_FILTER, useClass: ProblemDetailsFilter }
      ]
    }).compile();

    app = modulo.createNestApplication();
    app.setGlobalPrefix("v1", { exclude: ["health"] });
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it("test_ca_health_publico_retorna_200_e_status_ok", async () => {
    const resposta = await request(app.getHttpServer()).get("/health");
    expect(resposta.status).toBe(200);
    expect(resposta.body).toEqual({ status: "ok" });
  });
});
