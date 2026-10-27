import matplotlib.pyplot as plt
import csv

isolates2 = []

with open("isolates2.csv", "r") as file:
    next(file, None)  # Skip the header

    for line in file:
        line = line.strip()

        # Remove the quotation marks around the entire row
        line = line.strip('"')

        data = line.split(",")

        if len(data) < 5:
            print("Skipping incomplete row:", data)
            continue

        isolate = {
            "name": data[0],
            "gram_stain": data[1],
            "replicate_1": data[2],
            "replicate_2": data[3],
            "replicate_3": data[4]
        }

        isolates2.append(isolate)

print(isolates2)


# ==================================================
# 2. DEFINE FUNCTIONS
# ==================================================

def parse_replicate(value):
    """Convert a CSV value into a number or None."""
    if value.strip().lower() in ("", "none"):
        return None

    try:
        return float(value)
    except ValueError:
        return None


def calculate_average(values):
    """Calculate the mean of a list of numbers."""
    if not values:
        return None

    return sum(values) / len(values)


def validate_replicates(values):
    """Validate the replicate measurements."""
    if any(value is not None and value < 0 for value in values):
        return "Invalid"

    if any(value is None for value in values):
        return "Missing data"

    return "Valid"


def interpret_zone(mean_zone):
    """Classify the mean zone using the exercise thresholds."""
    if mean_zone is None:
        return "Missing data"
    elif mean_zone < 10:
        return "Resistant"
    elif mean_zone < 20:
        return "Intermediate"
    else:
        return "Susceptible"


def calculate_percentage(count, total):
    """Calculate a percentage safely."""
    if total == 0:
        return 0

    return (count / total) * 100


def check_mean_zone(mean_zone):
    if mean_zone is None:
        return "Missing data"
    elif mean_zone < 0:
        return "Check required"
    elif 0 <= mean_zone <= 30:
        return "Within exercise range"
    else:
        return "Above exercise range"

# ==================================================
# 3. VALIDATE DATA AND CALCULATE MEANS
# ==================================================


valid_count = 0
missing_count = 0
invalid_count = 0

for isolate in isolates2:
    values = [
        parse_replicate(isolate["replicate_1"]),
        parse_replicate(isolate["replicate_2"]),
        parse_replicate(isolate["replicate_3"])
    ]

    # Store converted values back in the dictionary.
    isolate["replicate_1"] = values[0]
    isolate["replicate_2"] = values[1]
    isolate["replicate_3"] = values[2]

    result = validate_replicates(values)
    isolate["validation"] = result

    if result == "Valid":
        isolate["mean_zone"] = calculate_average(values)
        valid_count += 1

    else:
        isolate["mean_zone"] = None

        if result == "Missing data":
            missing_count += 1
        else:
            invalid_count += 1

    isolate["interpretation"] = interpret_zone(
        isolate["mean_zone"]
    )

    isolate["quality_check"] = check_mean_zone(
        isolate["mean_zone"]
    )

# ==================================================
# 4. DATA VALIDATION SUMMARY
# ==================================================

print("\nDATA VALIDATION SUMMARY")
print("-----------------------")

for isolate in isolates2:
    print(isolate["name"], isolate["validation"])

print("Valid isolates:", valid_count)
print("Isolates with missing data:", missing_count)
print("Invalid isolates:", invalid_count)


# ==================================================
# 5. MEAN ZONES AND INTERPRETATIONS
# ==================================================

print("\nISOLATE RESULTS")
print("---------------")

for isolate in isolates2:
    mean_zone = isolate["mean_zone"]

    if mean_zone is None:
        mean_text = "Missing"
    else:
        mean_text = f"{mean_zone:.2f} mm"

    print(
        f"{isolate['name']} | "
        f"Mean zone: {mean_text} | "
        f"Interpretation: {isolate['interpretation']}"
    )
    print("Quality check:", isolate["quality_check"])

# ==================================================
# 6. HIGHEST AND LOWEST MEAN ZONES
# ==================================================

valid_isolates = [
    isolate for isolate in isolates2
    if isolate["mean_zone"] is not None
]

print("\nHIGHEST AND LOWEST MEAN ZONES")
print("-----------------------------")

if valid_isolates:
    highest = max(
        valid_isolates,
        key=lambda isolate: isolate["mean_zone"]
    )

    lowest = min(
        valid_isolates,
        key=lambda isolate: isolate["mean_zone"]
    )

    print(
        f"Highest: {highest['name']} "
        f"({highest['mean_zone']:.2f} mm)"
    )

    print(
        f"Lowest: {lowest['name']} "
        f"({lowest['mean_zone']:.2f} mm)"
    )
else:
    print("No valid mean zones are available.")


# ==================================================
# 7. SUSCEPTIBILITY SUMMARY
# ==================================================

resistant_isolates = []
intermediate_isolates = []
susceptible_isolates = []

for isolate in valid_isolates:
    interpretation = isolate["interpretation"]

    if interpretation == "Resistant":
        resistant_isolates.append(isolate["name"])
    elif interpretation == "Intermediate":
        intermediate_isolates.append(isolate["name"])
    elif interpretation == "Susceptible":
        susceptible_isolates.append(isolate["name"])


resistant_count = len(resistant_isolates)
intermediate_count = len(intermediate_isolates)
susceptible_count = len(susceptible_isolates)

print("\nSUSCEPTIBILITY SUMMARY")
print("----------------------")

print("Resistant isolates:", resistant_isolates)
print("Intermediate isolates:", intermediate_isolates)
print("Susceptible isolates:", susceptible_isolates)

print(
    f"Resistant: "
    f"{calculate_percentage(resistant_count, valid_count):.2f}%"
)
print(
    f"Intermediate: "
    f"{calculate_percentage(intermediate_count, valid_count):.2f}%"
)
print(
    f"Susceptible: "
    f"{calculate_percentage(susceptible_count, valid_count):.2f}%"
)

percentage_total = (
    calculate_percentage(resistant_count, valid_count)
    + calculate_percentage(intermediate_count, valid_count)
    + calculate_percentage(susceptible_count, valid_count)
)

if valid_count > 0 and round(percentage_total, 2) == 100:
    print("Susceptibility percentages add up to 100%.")


# ==================================================
# 8. OVERALL MEAN ZONE
# ==================================================

print("\nOVERALL SUMMARY")
print("---------------")

if valid_isolates:
    overall_mean = calculate_average(
        [isolate["mean_zone"] for isolate in valid_isolates]
    )
    print(f"Overall mean zone: {overall_mean:.2f} mm")
else:
    print("Overall mean cannot be calculated: no valid data.")


# ==================================================
# 9. GRAM-STAIN GROUP SUMMARY
# ==================================================

gram_negative_isolates = [
    isolate for isolate in valid_isolates
    if isolate["gram_stain"] == "Gram-negative"
]

gram_positive_isolates = [
    isolate for isolate in valid_isolates
    if isolate["gram_stain"] == "Gram-positive"
]

gram_negative_count = len(gram_negative_isolates)
gram_positive_count = len(gram_positive_isolates)

gram_negative_mean = calculate_average(
    [isolate["mean_zone"] for isolate in gram_negative_isolates]
)

gram_positive_mean = calculate_average(
    [isolate["mean_zone"] for isolate in gram_positive_isolates]
)

print("\nGRAM-STAIN SUMMARY")
print("------------------")

print("Total isolates:", len(isolates2))
print("Valid isolates:", valid_count)
print("Gram-negative isolates:", gram_negative_count)
print("Gram-positive isolates:", gram_positive_count)

print(
    f"Gram-negative percentage: "
    f"{calculate_percentage(gram_negative_count, valid_count):.2f}%"
)
print(
    f"Gram-positive percentage: "
    f"{calculate_percentage(gram_positive_count, valid_count):.2f}%"
)

if gram_negative_mean is not None:
    print(f"Gram-negative mean zone: {gram_negative_mean:.2f} mm")
else:
    print("Gram-negative mean zone: Not available")

if gram_positive_mean is not None:
    print(f"Gram-positive mean zone: {gram_positive_mean:.2f} mm")
else:
    print("Gram-positive mean zone: Not available")


# ==================================================
# 10. COMPARE GRAM-STAIN GROUP MEANS
# ==================================================

print("\nGRAM-STAIN GROUP COMPARISON")
print("---------------------------")

if gram_negative_mean is not None and gram_positive_mean is not None:
    mean_difference = gram_positive_mean - gram_negative_mean

    print(f"Mean difference: {mean_difference:.2f} mm")

    if gram_positive_mean > gram_negative_mean:
        print("Gram-positive isolates have the higher mean zone.")
    elif gram_negative_mean > gram_positive_mean:
        print("Gram-negative isolates have the higher mean zone.")
    else:
        print("The two groups have the same mean zone.")

    if gram_negative_mean != 0:
        percentage_difference = (
            mean_difference / gram_negative_mean
        ) * 100

        print(
            f"Difference relative to Gram-negative mean: "
            f"{percentage_difference:.2f}%"
        )
    else:
        print(
            "Relative percentage difference cannot be calculated "
            "because the Gram-negative mean is zero."
        )
else:
    print("At least one group has no valid mean for comparison.")

# ==================================================
# 11. EXPORT RESULTS TO CSV
# ==================================================


output_file = "isolate_analysis_results.csv"

fieldnames = [
    "name",
    "gram_stain",
    "replicate_1",
    "replicate_2",
    "replicate_3",
    "validation",
    "mean_zone",
    "interpretation",
    "quality_check"
]

with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for isolate in isolates2:
        writer.writerow(isolate)

print("\nEXPORT COMPLETE")
print("----------------")
print("Results saved to:", output_file)


# ==================================================
# 12. PLOT MEAN ZONES OF INHIBITION
# ==================================================


# Keep only isolates with valid mean zones.
chart_isolates = [
    isolate for isolate in isolates2
    if isolate["mean_zone"] is not None
]

if chart_isolates:
    names = [
        isolate["name"] for isolate in chart_isolates
    ]

    means = [
        isolate["mean_zone"] for isolate in chart_isolates
    ]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(names, means)

    plt.title("Mean Zones of Inhibition by Isolate")
    plt.xlabel("Bacterial Isolate")
    plt.ylabel("Mean Zone of Inhibition (mm)")

    plt.xticks(rotation=30, ha="right")

    # Display the mean above each bar.
    for bar, mean in zip(bars, means):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{mean:.2f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    chart_file = "mean_zone_by_isolate.png"
    plt.savefig(chart_file, dpi=300, bbox_inches="tight")

    print("\nCHART EXPORTED")
    print("--------------")
    print("Chart saved to:", chart_file)

    plt.show()

else:
    print("No valid mean zones available for plotting.")
