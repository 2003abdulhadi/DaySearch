from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
api = Api(app)

# Create the engine and session
engine = create_engine('sqlite:///job_postings.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class JobPosting(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True)
    role = Column(String)
    company = Column(String)
    posted_date = Column(Date)
    deadline = Column(Date)
    experience_level = Column(String)


class JobPostingsResource(Resource):
    def get(self):
        # Retrieve query parameters from the request
        role = request.args.get('role')
        company = request.args.get('company')
        experience_level = request.args.get('experience_level')

        # Prepare the base query
        query = session.query(JobPosting)

        # Apply filters based on query parameters
        if role:
            query = query.filter(JobPosting.role == role)
        if company:
            query = query.filter(JobPosting.company == company)
        if experience_level:
            query = query.filter(JobPosting.experience_level == experience_level)

        # Execute the query and retrieve the job postings
        job_postings = query.all()

        # Return the job postings as a response
        # You can serialize the job postings as per your preference
        # For example, convert them to JSON format
        serialized_job_postings = [job_posting.to_dict() for job_posting in job_postings]
        return serialized_job_postings, 200

    def post(self):
        # Implement logic to create a new job posting
        pass


class JobPostingResource(Resource):
    def get(self, job_id):
        # Retrieve the job posting with the specified ID
        job_posting = session.query(JobPosting).filter(JobPosting.id == job_id).first()

        if not job_posting:
            return {'message': 'Job posting not found'}, 404

        # Return the job posting as a response
        # You can serialize the job posting as per your preference
        # For example, convert it to JSON format
        serialized_job_posting = job_posting.to_dict()
        return serialized_job_posting, 200


api.add_resource(JobPostingsResource, '/job_postings')
api.add_resource(JobPostingResource, '/job_postings/<int:job_id>')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
