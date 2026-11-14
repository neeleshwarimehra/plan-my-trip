interface DestinationCardProps {
  name: string;
  country: string;
  description: string;
  image: string;
  price: string;
  onSelect?: (destinationName: string, price: string) => void;
}

function DestinationCard({
  name,
  country,
  description,
  image,
  price,
  onSelect,
}: DestinationCardProps) {
  return (
    <article className="destination-card">
      <img src={image} alt={name} />

      <div className="destination-info">
        <span className="destination-country">{country}</span>
        <h3>{name}</h3>
        <p>{description}</p>

        <div className="destination-bottom">
          <span>From {price}</span>
          <button
            type="button"
            aria-label={`Explore ${name}`}
            onClick={() => onSelect?.(name, price)}
          >
            →
          </button>
        </div>
      </div>
    </article>
  );
}

export default DestinationCard;