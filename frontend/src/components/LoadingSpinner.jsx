export default function LoadingSpinner() {
  return (
    <div className="flex justify-center py-16" role="status" aria-label="Loading">
      <div className="w-8 h-8 border-2 border-neutral-300 border-t-neutral-900 rounded-full animate-spin" />
    </div>
  );
}
