interface WeakAreasProps {
  weakAreas?: string[];
}

function WeakAreas({ weakAreas = [] }: WeakAreasProps) {
  return (
    <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-4">Weak Areas</h2>

      {weakAreas.length === 0 ? (
        <p className="text-slate-500">
          Great job! No major weak areas detected 🎉
        </p>
      ) : (
        <div className="flex flex-wrap gap-3">
          {weakAreas.map((area, index) => (
            <span
              key={index}
              className="px-4 py-2 rounded-full bg-red-50 text-red-700 border border-red-200 text-sm font-medium"
            >
              {area}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default WeakAreas;