import { Injectable, OnModuleDestroy, OnModuleInit } from "@nestjs/common";
import { PrismaClient } from "@prisma/client";
import { Inject } from "@nestjs/common";
import { ENV, Env } from "../env";

// Conexão de runtime via DATABASE_URL (pooler na Vercel);
// migrations usam directUrl (ADR-001, seção 5).
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor(@Inject(ENV) env: Env) {
    super({
      datasources: {
        db: { url: env.DATABASE_URL }
      }
    });
  }

  async onModuleInit(): Promise<void> {
    await this.$connect();
  }

  async onModuleDestroy(): Promise<void> {
    await this.$disconnect();
  }
}
