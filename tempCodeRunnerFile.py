elif programa == "Grafico":
        # Plot the stock vs the hour of the day

    plt.figure(figsize=(10, 6))
    for flavor in existing_df['Helado'].unique():
        flavor_df = existing_df[existing_df['Helado'] == flavor]
        plt.plot(flavor_df['Hora'], flavor_df['Stock'], label=flavor)

    plt.xlabel('Hour of the Day')
    plt.ylabel('Stock')
    plt.title('Stock vs Hour of the Day')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()