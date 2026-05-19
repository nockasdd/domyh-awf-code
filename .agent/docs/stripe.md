---
library: stripe
version: latest
latest: true
category: payments
official_docs: https://docs.stripe.com
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# Stripe

> Stripe — Payment processing platform for internet businesses.
> Docs: https://docs.stripe.com

## Installation

```bash
npm install stripe          # Server SDK
npm install @stripe/stripe-js  # Client SDK
npm install @stripe/react-stripe-js  # React components
```

## Server-Side (Node.js)

```ts
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Create Payment Intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,        // $20.00 (in cents)
  currency: 'usd',
  automatic_payment_methods: { enabled: true },
  metadata: { order_id: '12345' },
});

// Create Checkout Session
const session = await stripe.checkout.sessions.create({
  mode: 'payment',       // 'payment' | 'subscription' | 'setup'
  line_items: [{
    price: 'price_xxxxx',  // Stripe Price ID
    quantity: 1,
  }],
  success_url: 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://example.com/cancel',
});

// Create Customer + Subscription
const customer = await stripe.customers.create({ email: 'user@example.com' });
const subscription = await stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: 'price_monthly' }],
});
```

## Client-Side (React)

```tsx
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!stripe || !elements) return;

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: { return_url: 'https://example.com/success' },
    });

    if (error) console.error(error.message);
  };

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button disabled={!stripe}>Pay</button>
    </form>
  );
}

// Wrap with Elements provider
<Elements stripe={stripePromise} options={{ clientSecret }}>
  <CheckoutForm />
</Elements>
```

## Webhooks

```ts
// app/api/webhooks/stripe/route.ts (Next.js)
import Stripe from 'stripe';

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature')!;

  const event = stripe.webhooks.constructEvent(
    body,
    sig,
    process.env.STRIPE_WEBHOOK_SECRET!
  );

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      await fulfillOrder(session);
      break;
    case 'invoice.paid':
      await activateSubscription(event.data.object);
      break;
    case 'customer.subscription.deleted':
      await cancelSubscription(event.data.object);
      break;
  }

  return new Response('OK', { status: 200 });
}
```

## API Versioning

```ts
// Pin API version explicitly (recommended)
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-06-20',  // latest stable version
});

// Backward-compatible changes:
// - Adding new API resources/optional params
// - Adding new properties to responses
// - Adding new event types
// Forward-breaking changes require explicit version upgrade
```

## Stripe CLI

```bash
# Install: https://docs.stripe.com/stripe-cli
stripe login                        # authenticate
stripe listen --forward-to localhost:3000/api/webhooks/stripe  # forward webhooks
stripe trigger checkout.session.completed   # trigger test event
stripe logs tail                    # view API logs in real-time
stripe resources                    # explore API resources
```

## Customer Portal (Subscriptions)

```ts
// Create portal session for subscription management
const portalSession = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: 'https://example.com/account',
});
// Redirect customer to portalSession.url
```

## Billing (Subscriptions)

```ts
// Create subscription with Checkout Sessions (recommended)
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: customerId,
  line_items: [{
    price: 'price_monthly_pro',  // recurring price ID
    quantity: 1,
  }],
  success_url: 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://example.com/cancel',
});

// Usage-based billing
const price = await stripe.prices.create({
  currency: 'usd',
  unit_amount: 10,  // $0.10 per unit
  recurring: { interval: 'month', usage_type: 'metered' },
  product: 'prod_xxx',
});

// Record usage
await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
  quantity: 100,
  timestamp: Math.floor(Date.now() / 1000),
  action: 'increment',
});

// Cancel subscription
await stripe.subscriptions.update(subId, {
  cancel_at_period_end: true,  // cancel at end of billing period
});
```

## Connect (Platforms & Marketplaces)

```ts
// Create connected account (Standard)
const account = await stripe.accounts.create({
  type: 'standard',
  country: 'US',
  email: 'seller@example.com',
});

// Create account link for onboarding
const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: 'https://example.com/reauth',
  return_url: 'https://example.com/return',
  type: 'account_onboarding',
});

// Direct charge (platform takes fee)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'usd',
  application_fee_amount: 200,  // platform takes $2
}, {
  stripeAccount: connectedAccountId,  // charge on connected account
});

// Transfer to connected account
const transfer = await stripe.transfers.create({
  amount: 1800,
  currency: 'usd',
  destination: connectedAccountId,
});
```

## LLM Integration Best Practices

> From Stripe's official llms.txt guidance for AI agents:

- **Always use Checkout Sessions API** — primary backend object for payments
- **Use Payment Element** for frontend — never recommend legacy Card Element
- **Never use deprecated APIs**: Sources API, Tokens API, Charges API
- **Use Setup Intent** to save payment methods (not Sources API)
- **Enable dynamic payment methods** in dashboard instead of hardcoding `payment_method_types`
- **For SaaS/recurring**: Use Billing APIs + Stripe Checkout, not raw PaymentIntents
- **For PAN migration**: Use Stripe's data migration process

## Gotchas

⚠️ **Amounts in cents**: `amount: 2000` = $20.00.

⚠️ **Webhook verification**: Always verify `stripe-signature` — never trust raw POST body.

⚠️ **Test mode**: Use `sk_test_` / `pk_test_` keys for development.

⚠️ **Idempotency**: Use `idempotencyKey` for retryable requests.

⚠️ **API versioning**: Pin version explicitly in Stripe constructor. Latest: `2024-06-20`.

⚠️ **Stripe CLI**: Use `stripe listen` to forward webhooks during local development.

⚠️ **Checkout Sessions API**: Always prefer over PaymentIntents API for new integrations.

⚠️ **Connect**: Use `stripeAccount` header for direct charges on connected accounts.

⚠️ **Billing**: Use `cancel_at_period_end: true` instead of immediate cancellation.
