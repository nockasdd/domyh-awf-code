---
name: payment-integration
description: Payment gateway & bank monitoring integration for 10 providers (VN + Global)
detect: ["*stripe*", "*paypal*", "*payment*"]
category: cross-cutting
tier: 1
---

# 💳 Payment Integration Skill

> 10 providers: VNPay, MoMo, ZaloPay, Pay2S, payOS, SePay, Casso, Stripe, PayPal, Razorpay
> 📊 API specs, webhook/IPN, signature verification, security patterns
> 📁 Data: `.agent/skills/cross-cutting/payment-integration/data/`

## When to Use

- Integrating a payment provider (gateway or bank monitoring)
- Building checkout flow / payment link creation
- Handling webhook/IPN callbacks
- Implementing signature verification & security
- Setting up sandbox/test environment

## Provider Categories

| Category | Providers | Flow |
|----------|-----------|------|
| **VN Gateways** | VNPay, MoMo, ZaloPay | Create URL/session → redirect → IPN callback |
| **VN Bank Monitors** | Pay2S, payOS, SePay, Casso | Create link → VietQR scan → webhook notify |
| **Global** | Stripe, PayPal, Razorpay | Create intent/order → checkout → webhook event |

## Integration Steps

### Step 1: Identify Provider
Match user request to provider in `data/providers.yaml`. Check:
- Region (Vietnam vs Global)
- Type (gateway vs bank monitor vs full platform)
- Payment methods needed (QR, card, wallet, bank transfer)

### Step 2: Load Provider Data
Query `data/providers.yaml` for:
- Sandbox & production URLs
- Authentication method & keys
- Create payment API (method, params, amount handling)
- Required environment variables

### Step 3: Generate Integration Code
Based on provider, generate:
1. **Create payment** — API call to create payment URL/session/intent
2. **Webhook handler** — Endpoint to receive provider callbacks
3. **Signature verification** — Verify data integrity per `data/security.yaml`
4. **Order update** — Atomic status update in database

### Step 4: Apply Security
Load `data/security.yaml` and ensure:
- Signature/HMAC verification before processing
- Idempotency (duplicate webhook handling)
- Amount/currency verification against DB
- HTTPS for webhook endpoints
- Audit logging of all callbacks

### Step 5: Configure Sandbox
Load sandbox config from `data/providers.yaml`:
- Test API keys/URLs
- Test card numbers / bank accounts
- Sandbox-specific behavior differences

## Pre-delivery Checklist

### Security ✅
- [ ] Signature/HMAC verification implemented
- [ ] Amount matches order in database
- [ ] Currency verification
- [ ] HTTPS webhook endpoint
- [ ] Secrets stored in environment variables (NEVER in code)

### Reliability ✅
- [ ] Idempotency — duplicate webhooks handled gracefully
- [ ] Return 200/success FAST (before complex logic)
- [ ] Order status checked before processing (skip if already done)
- [ ] Database transaction for atomic order update
- [ ] Timeout on provider API calls (30s max)

### User Experience ✅
- [ ] Return URL handles display only (not order update)
- [ ] Error/timeout shows "payment processing" message
- [ ] Cancel URL properly handles order cancellation

### Testing ✅
- [ ] Sandbox configuration included
- [ ] Test payment flow documented
- [ ] Webhook testing instructions provided
