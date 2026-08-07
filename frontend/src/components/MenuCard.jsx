export default function MenuCard({ item, onAdd }) {
  return (
    <div className="group border border-neutral-200 rounded-2xl p-4 flex flex-col justify-between bg-white hover:shadow-md transition-shadow">
      <div>
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-medium text-neutral-900">{item.name}</h3>
          <span className="text-xs px-2 py-0.5 rounded-full bg-neutral-100 text-neutral-500 whitespace-nowrap">
            {item.category}
          </span>
        </div>
        {item.description && (
          <p className="text-sm text-neutral-500 mt-1.5 line-clamp-2">
            {item.description}
          </p>
        )}
      </div>
      <div className="flex items-center justify-between mt-4">
        <span className="font-semibold text-neutral-900">
          ₹{item.price.toFixed(2)}
        </span>
        <button
          onClick={onAdd}
          className="px-3.5 py-1.5 rounded-lg bg-neutral-900 text-white text-sm font-medium hover:bg-neutral-700 transition-colors"
        >
          Add
        </button>
      </div>
    </div>
  );
}
