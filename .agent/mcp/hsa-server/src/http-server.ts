#!/usr/bin/env node
/**
 * HSA v5.0 HTTP Server Entry Point
 * Run with: npm run start:http
 */

import { startHttpServer } from "./http-transport.js";

const PORT = parseInt(process.env.PORT || "3000");
startHttpServer(PORT);
