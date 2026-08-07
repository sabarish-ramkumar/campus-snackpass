export default function CartSummary({ total }) {
  return (
    <div className="flex items-center justify-between mt-4 pt-4 border-t border-neutral-200">
      <span className="font-medium text-neutral-700">Total</span>
      <span className="font-semibold text-lg text-neutral-900">
        ₹{total.toFixed(2)}
      </span>
    </div>
  );
}
