export default function CartItem({ item, onRemove, onQuantityChange }) {
  return (
    <div className="flex items-center justify-between border border-neutral-200 rounded-xl p-3 bg-white">
      <div>
        <p className="font-medium text-neutral-900">{item.name}</p>
        <p className="text-sm text-neutral-500">₹{item.price.toFixed(2)} each</p>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <button
            onClick={() => onQuantityChange(item.quantity - 1)}
            aria-label={`Decrease quantity of ${item.name}`}
            className="w-7 h-7 rounded-full border border-neutral-300 hover:bg-neutral-50"
          >
            −
          </button>
          <span className="w-5 text-center tabular-nums">{item.quantity}</span>
          <button
            onClick={() => onQuantityChange(item.quantity + 1)}
            aria-label={`Increase quantity of ${item.name}`}
            className="w-7 h-7 rounded-full border border-neutral-300 hover:bg-neutral-50"
          >
            +
          </button>
        </div>
        <button
          onClick={onRemove}
          className="text-sm text-red-600 hover:text-red-700"
        >
          Remove
        </button>
      </div>
    </div>
  );
}
