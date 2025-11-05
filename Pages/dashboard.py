import streamlit as st
import numpy as np
from supabase import create_client
from openai import OpenAI  # ou outro modelo de embeddings
import os

st.subheader("📊 Dashboards", divider="rainbow", anchor=False)


