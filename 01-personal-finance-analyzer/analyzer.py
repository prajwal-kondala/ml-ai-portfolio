"""
Personal Finance Analyzer
Author: Prajwal Kondala
Date: February 2026
Description: Analyzes bank transactions and generates spending reports
"""

import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def load_transactions(filename):
    """Load transactions from CSV file"""
    transactions = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['amount'] = float(row['amount'])
            transactions.append(row)
    return transactions

def calculate_total_spending(transactions):
    """Calculate total amount spent"""
    return sum(t['amount'] for t in transactions)

def spending_by_category(transactions):
    """Calculate spending by each category"""
    category_totals = defaultdict(float)
    for t in transactions:
        category_totals[t['category']] += t['amount']
    return dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))

def monthly_breakdown(transactions):
    """Break down spending by month"""
    monthly_totals = defaultdict(float)
    for t in transactions:
        month = t['date'][:7]
        monthly_totals[month] += t['amount']
    return dict(sorted(monthly_totals.items()))

def top_transactions(transactions, n=5):
    """Get top N highest transactions"""
    return sorted(transactions, key=lambda x: x['amount'], reverse=True)[:n]

def generate_report(transactions):
    """Generate comprehensive text report"""
    total = calculate_total_spending(transactions)
    by_category = spending_by_category(transactions)
    monthly = monthly_breakdown(transactions)
    top_5 = top_transactions(transactions, 5)
    
    report = []
    report.append("=" * 70)
    report.append("           PERSONAL FINANCE ANALYSIS REPORT")
    report.append("=" * 70 + "\\n")
    
    report.append("SUMMARY")
    report.append("-" * 70)
    report.append(f"Total Transactions: {len(transactions)}")
    report.append(f"Total Spending: ₹{total:,.2f}")
    report.append(f"Average Transaction: ₹{total/len(transactions):,.2f}\\n")
    
    report.append("SPENDING BY CATEGORY")
    report.append("-" * 70)
    for category, amount in by_category.items():
        percentage = (amount / total) * 100
        report.append(f"{category.capitalize():15} ₹{amount:10,.2f}  ({percentage:5.1f}%)")
    
    return "\\n".join(report)

def plot_category_spending(spending_dict):
    """Create bar chart of spending by category"""
    categories = list(spending_dict.keys())
    amounts = list(spending_dict.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, amounts, color='steelblue', edgecolor='black')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:,.0f}', ha='center', va='bottom')
    
    plt.xlabel('Category', fontweight='bold')
    plt.ylabel('Amount Spent (₹)', fontweight='bold')
    plt.title('Spending by Category', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('category_spending.png', dpi=300, bbox_inches='tight')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Load data
    transactions = load_transactions('transactions.csv')
    
    # Generate analysis
    print("Loading transactions...")
    print(f"✓ Loaded {len(transactions)} transactions\\n")
    
    # Calculate statistics
    total = calculate_total_spending(transactions)
    by_category = spending_by_category(transactions)
    
    # Display results
    print(f"Total Spending: ₹{total:,.0f}\\n")
    print("Category Breakdown:")
    for cat, amount in by_category.items():
        print(f"  {cat.capitalize()}: ₹{amount:,.0f}")
    
    # Generate report
    report = generate_report(transactions)
    print("\\n" + report)
    
    # Create visualization
    plot_category_spending(by_category)
    
    print("\\n✓ Analysis complete!")
