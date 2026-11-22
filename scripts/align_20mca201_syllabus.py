import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import db, Course, Module, Topic, UserProgress

# Exact Module and Topic definition from KTU MCA Scheme 2020 Syllabus (pages 168-171)
SYLLABUS_20MCA201 = [
    {
        "module_no": 1,
        "name": "Module 1: Data Science Foundations & Visualization",
        "hours": 9,
        "topics": [
            "Data science lifecycle",
            "Data collection, and cleaning",
            "Preprocessing and data preparation",
            "Data science classification and process: Prior knowledge, Data preparation, Modelling, Application",
            "Data exploration: Data sets, Descriptive statistics for univariate and multivariate data",
            "Data visualization: Histogram, Quartile plot, Distribution chart, Scatter plot, Bubble chart, Density chart"
        ]
    },
    {
        "module_no": 2,
        "name": "Module 2: Machine Learning & Lazy/Probabilistic Learners",
        "hours": 9,
        "topics": [
            "How machines learn: Data storage, Abstraction, Generalisation, Evaluation",
            "Machine learning in practice: Types of machine learning algorithms",
            "Lazy learning: Classification using K-Nearest Neighbour (k-NN) algorithm",
            "Measuring similarity, Choice of k",
            "Preparing data for use with k-NN",
            "Probabilistic learning: Conditional probability and Bayes theorem",
            "Naive Bayes algorithm and Laplace estimator"
        ]
    },
    {
        "module_no": 3,
        "name": "Module 3: Decision Trees & Regression Methods",
        "hours": 9,
        "topics": [
            "Decision tree learning: Concept of decision tree, Divide and conquer approach",
            "C5.0 Decision tree algorithm",
            "Choosing the best split, Pruning the decision tree",
            "Classification rules learning: Concept of classification rules, Separate and conquer approach",
            "The 1R algorithm, Rules from decision trees",
            "Regression methods: Concept of regression, Correlations",
            "Simple linear regression, Ordinary least squares estimation",
            "Multiple linear regression"
        ]
    },
    {
        "module_no": 4,
        "name": "Module 4: Neural Networks & Support Vector Machines",
        "hours": 9,
        "topics": [
            "Understanding neural networks: Artificial neurons",
            "Activation functions and Network topology",
            "Training neural networks with back propagation",
            "Understanding Support Vector Machines: Classification with hyperplane",
            "Linearly separable data and Nonlinearly separable data",
            "Methods to find maximum margin hyperplanes in linearly separable data",
            "Using kernels for non-linear spaces"
        ]
    },
    {
        "module_no": 5,
        "name": "Module 5: Clustering & Model Evaluation",
        "hours": 9,
        "topics": [
            "Understanding Clustering: The k-means clustering algorithm",
            "Using distance to assign and update clusters, Choosing the appropriate number of clusters",
            "Evaluating model performance: Confusion matrices, Precision and recall, Sensitivity and specificity, F-measure, ROC curves",
            "Cross validation: K-fold cross validation, Bootstrap sampling",
            "Improving model performance: Bagging, Boosting",
            "Random forests"
        ]
    }
]


def run_alignment():
    with app.app_context():
        course = Course.query.filter_by(code="20MCA201").first()
        if not course:
            print("Course 20MCA201 not found!")
            return

        print(f"Aligning Course: {course.code} - {course.name}")

        for mod_data in SYLLABUS_20MCA201:
            m_no = mod_data["module_no"]
            module = Module.query.filter_by(course_id=course.id, module_no=m_no).first()
            if not module:
                module = Module(
                    name=mod_data["name"],
                    module_no=m_no,
                    hours=mod_data["hours"],
                    course_id=course.id
                )
                db.session.add(module)
                db.session.flush()
            else:
                module.name = mod_data["name"]
                module.hours = mod_data["hours"]

            # Clear all old topics in this module to avoid mixed/corrupted topics
            for t in list(module.topics):
                UserProgress.query.filter_by(topic_id=t.id).delete()
                db.session.delete(t)
            db.session.flush()

            # Insert exact official topics with sequential topic numbers
            for idx, title in enumerate(mod_data["topics"], 1):
                new_t = Topic(name=title, topic_no=idx, module_id=module.id)
                db.session.add(new_t)
                db.session.flush()

                # Mark student progress: user 1 completed module 1 first 3 topics and module 5 topics
                completed = False
                if m_no == 1 and idx in [1, 2, 3]:
                    completed = True
                elif m_no == 5:
                    completed = True

                prog = UserProgress(user_id=1, topic_id=new_t.id, completed=completed)
                db.session.add(prog)

        db.session.commit()
        print("Syllabus alignment for 20MCA201 completed successfully with clean sequential numbering!")


if __name__ == "__main__":
    run_alignment()
