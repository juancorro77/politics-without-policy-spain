import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # 1. Load the dataset
    csv_path = "data/processed/classified_dataset.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please run the analysis script first.")
        return
        
    df = pd.read_csv(csv_path)
    
    # Filter for policy-manifest questions with active debate
    policy_df = df[
        (df["manifest_topic"] == "policy") & 
        ((df["total_policy_ud"] + df["total_politics_ud"]) > 0)
    ].copy()
    
    # Ensure legislature is treated as string for mapping to palette keys
    policy_df["legislature"] = policy_df["legislature"].astype(str)
    
    # 2. Set styling configurations for high-quality academic publishing
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    plt.rcParams["svg.fonttype"] = "none" # Keep text editable in SVGs
    
    # Create output directory
    figures_dir = "paper/figures"
    os.makedirs(figures_dir, exist_ok=True)
    
    # Define cohesive, academic color palette (soft blue and muted coral/red)
    palette_leg = {"14": "#4A90E2", "15": "#E25A53"} 
    
    print(f"Loaded {len(policy_df)} policy debates to plot.")
    
    # -------------------------------------------------------------
    # FIGURE 1: Violin & Boxplots of ASR and ER by Legislature
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.5), sharey=True)
    
    # Customize layout style
    sns.set_style("whitegrid", {"grid.linestyle": "--", "grid.alpha": 0.5})
    
    # Panel A: Agenda Shift Rate (ASR)
    sns.violinplot(
        data=policy_df, 
        x="legislature", 
        y="ASR", 
        hue="legislature",
        legend=False,
        ax=axes[0], 
        palette=palette_leg, 
        inner=None, 
        alpha=0.25,
        linewidth=1.2
    )
    sns.boxplot(
        data=policy_df, 
        x="legislature", 
        y="ASR", 
        hue="legislature",
        legend=False,
        ax=axes[0], 
        palette=palette_leg, 
        width=0.25, 
        boxprops=dict(alpha=0.8),
        showfliers=False
    )
    # Superimpose individual data points with low opacity to show distribution density
    sns.stripplot(
        data=policy_df, 
        x="legislature", 
        y="ASR", 
        ax=axes[0], 
        color="#2c3e50", 
        alpha=0.3, 
        size=4, 
        jitter=0.15
    )
    
    axes[0].set_title("Agenda Shift Rate (ASR)", fontsize=14, fontweight="bold", pad=15)
    axes[0].set_xlabel("Legislature", fontsize=12, labelpad=10)
    axes[0].set_ylabel("Percentage (%)", fontsize=12)
    axes[0].set_xticklabels(["XIV (2019-2023)", "XV (2023-Present)"])
    axes[0].set_ylim(-5, 105)
    
    # Panel B: Minister Evasion Rate (ER)
    sns.violinplot(
        data=policy_df, 
        x="legislature", 
        y="ER", 
        hue="legislature",
        legend=False,
        ax=axes[1], 
        palette=palette_leg, 
        inner=None, 
        alpha=0.25,
        linewidth=1.2
    )
    sns.boxplot(
        data=policy_df, 
        x="legislature", 
        y="ER", 
        hue="legislature",
        legend=False,
        ax=axes[1], 
        palette=palette_leg, 
        width=0.25, 
        boxprops=dict(alpha=0.8),
        showfliers=False
    )
    sns.stripplot(
        data=policy_df, 
        x="legislature", 
        y="ER", 
        ax=axes[1], 
        color="#2c3e50", 
        alpha=0.3, 
        size=4, 
        jitter=0.15
    )
    
    axes[1].set_title("Minister Evasion Rate (ER)", fontsize=14, fontweight="bold", pad=15)
    axes[1].set_xlabel("Legislature", fontsize=12, labelpad=10)
    axes[1].set_ylabel("") # Hide y-label as it shares y-axis
    axes[1].set_xticklabels(["XIV (2019-2023)", "XV (2023-Present)"])
    
    # Remove top/right spines for cleaner look
    for ax in axes:
        sns.despine(ax=ax)
        
    plt.suptitle("Distribution of Deliberative Scrutiny Metrics by Legislature", fontsize=16, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save Figure 1
    fig1_path = os.path.join(figures_dir, "figure_1_distributions.png")
    fig1_pdf = os.path.join(figures_dir, "figure_1_distributions.pdf")
    plt.savefig(fig1_path, dpi=300)
    plt.savefig(fig1_pdf, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 1: {fig1_path} and {fig1_pdf}")
    
    # -------------------------------------------------------------
    # FIGURE 2: Scatter Plot of Party Metrics
    # -------------------------------------------------------------
    # Aggregate statistics by party group
    party_stats = policy_df.groupby("group").agg(
        mean_asr=("ASR", "mean"),
        mean_er=("ER", "mean"),
        initiatives_count=("id", "count")
    ).reset_index()
    
    # Filter out groups with very few initiatives to keep plot readable (threshold >= 3)
    party_stats = party_stats[party_stats["initiatives_count"] >= 3].copy()
    
    plt.figure(figsize=(10, 7))
    sns.set_style("whitegrid", {"grid.linestyle": "--", "grid.alpha": 0.5})
    
    # Create scatter plot: X=ASR, Y=ER, Size=Number of initiatives
    scatter = sns.scatterplot(
        data=party_stats,
        x="mean_asr",
        y="mean_er",
        size="initiatives_count",
        sizes=(150, 800),
        color="#34495e",
        alpha=0.85,
        edgecolor="black",
        linewidth=1.2,
        legend="brief"
    )
    
    # Annotate party names with a slight offset to prevent overlap
    # We define manual coordinate offsets based on party names for perfect legibility
    offsets = {
        "GP (PP)": (1.0, -0.5),
        "GVOX (Vox)": (-4.5, 1.2),
        "GR (ERC)": (1.0, -1.0),
        "GSUMAR (Sumar)": (1.0, 1.0),
        "GCs (Ciudadanos - XIV)": (-5.5, -2.2),
        "GJxCAT (Junts)": (-2.0, -2.5),
        "GPlu (Plural)": (1.0, 1.0),
    }
    
    for _, row in party_stats.iterrows():
        party_name = row["group"]
        
        # Clean up party names for display
        display_name = party_name
        if party_name == "GP":
            display_name = "PP"
        elif party_name == "GVOX":
            display_name = "VOX"
        elif party_name == "GR":
            display_name = "ERC"
        elif party_name == "GSUMAR":
            display_name = "SUMAR"
        elif party_name == "GCs":
            display_name = "Cs"
        elif party_name == "GJxCAT":
            display_name = "Junts"
        elif party_name == "GPlu":
            display_name = "Grupo Plural"
            
        dx, dy = offsets.get(party_name, (1.0, 1.0))
        
        plt.text(
            row["mean_asr"] + dx,
            row["mean_er"] + dy,
            display_name,
            fontsize=11,
            fontweight="bold",
            color="#2c3e50"
        )
        
    # Draw reference line at ASR and ER overall means
    overall_mean_asr = policy_df["ASR"].mean()
    overall_mean_er = policy_df["ER"].mean()
    
    plt.axvline(overall_mean_asr, color="#7f8c8d", linestyle=":", linewidth=1.5, label=f"Overall Mean ASR ({overall_mean_asr:.1f}%)")
    plt.axhline(overall_mean_er, color="#7f8c8d", linestyle=":", linewidth=1.5, label=f"Overall Mean ER ({overall_mean_er:.1f}%)")
    
    plt.title("Strategic Conflict Map: Party Positioning in Policy Control", fontsize=15, fontweight="bold", pad=20)
    plt.xlabel("Mean Agenda Shift Rate (ASR) provoked by Party (%)", fontsize=12, labelpad=10)
    plt.ylabel("Mean Evasion Rate (ER) of Ministers (%)", fontsize=12, labelpad=10)
    plt.xlim(55, 85)
    plt.ylim(55, 85)
    
    # Legend formatting
    handles, labels = scatter.get_legend_handles_labels()
    # Find indices for size labels
    size_handles = []
    size_labels = []
    for h, l in zip(handles, labels):
        if l.replace('.', '', 1).isdigit() or l.isdigit():
            size_handles.append(h)
            size_labels.append(l)
            
    # Add manual custom legend to explain size and mean lines
    plt.legend(
        size_handles, 
        size_labels, 
        title="Number of Policy Questions", 
        loc="lower left", 
        frameon=True,
        facecolor="white",
        edgecolor="#bdc3c7"
    )
    
    sns.despine()
    plt.tight_layout()
    
    # Save Figure 2
    fig2_path = os.path.join(figures_dir, "figure_2_party_positioning.png")
    fig2_pdf = os.path.join(figures_dir, "figure_2_party_positioning.pdf")
    plt.savefig(fig2_path, dpi=300)
    plt.savefig(fig2_pdf, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 2: {fig2_path} and {fig2_pdf}")

if __name__ == "__main__":
    main()
