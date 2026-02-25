"use client";

import React, { useState } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts';
import { 
  Activity, 
  Brain, 
  Mic, 
  CheckCircle2, 
  AlertCircle,
  FileText,
  Clock,
  BarChart3,
  Upload,
  Loader2,
  AlertTriangle
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// Global Feature Importance Data (from Training)
// These values represent the relative importance of features in the Random Forest model
const featureImportanceData = [
  { name: 'Pause Count', value: 23, color: '#3b82f6' },
  { name: 'Total Speech Time', value: 21, color: '#3b82f6' },
  { name: 'Pause/Word Ratio', value: 18, color: '#60a5fa' },
  { name: 'Total Pause Time', value: 15, color: '#60a5fa' },
  { name: 'Speech Rate', value: 13, color: '#93c5fd' },
  { name: 'Word Duration', value: 11, color: '#93c5fd' },
];

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [extractedFeatures, setExtractedFeatures] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setPrediction(null);
      setError(null);
      setExtractedFeatures(null);
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a .cha file first.");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);
    setExtractedFeatures(null);

    const formData = new FormData();
    formData.append("file", file);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

    try {
      // Connect to the actual Python backend
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Analysis failed");
      }

      const result = await response.json();
      setPrediction(result);
      setExtractedFeatures(result.features);
    } catch (err) {
      setError(err.message || "Failed to connect to the analysis server. Is the backend running?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 pb-20 font-sans text-slate-900 dark:text-slate-100">
      {/* Header */}
      <header className="bg-white dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent tracking-tight">NeuroVoice AI</h1>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">AD/MCI Detection System</p>
            </div>
          </div>
          <div className="flex gap-4">
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200 px-3 py-1 font-semibold flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              System Online
            </Badge>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 space-y-8 max-w-7xl">
        
        {/* Welcome Section */}
        <section className="space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">Project Overview</h2>
          <p className="text-slate-500 dark:text-slate-400 max-w-2xl text-lg">
            A machine learning system detecting Mild Cognitive Impairment (MCI) from vocal patterns.
            Upload a patient interview transcript (.cha) to analyze diagnostic biomarkers.
          </p>
        </section>

        {/* Key Metrics Cards (Static/Historical Data) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="hover:shadow-md transition-shadow border-slate-200 dark:border-slate-800">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Test Accuracy</CardTitle>
              <Activity className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">57.4%</div>
              <p className="text-xs text-slate-500 mt-1">
                Current Model Performance
              </p>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-md transition-shadow border-slate-200 dark:border-slate-800">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Control Class</CardTitle>
              <CheckCircle2 className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Healthy</div>
              <p className="text-xs text-slate-500 mt-1">
                Baseline Diagnosis
              </p>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-md transition-shadow border-slate-200 dark:border-slate-800">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Target Class</CardTitle>
              <AlertCircle className="h-4 w-4 text-amber-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">MCI / AD</div>
              <p className="text-xs text-slate-500 mt-1">
                Cognitive Impairment
              </p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-md transition-shadow border-slate-200 dark:border-slate-800">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Dataset Size</CardTitle>
              <FileText className="h-4 w-4 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">339</div>
              <p className="text-xs text-slate-500 mt-1">
                Patients Analyzed
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Feature Intelligence & Workflow */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Feature Importance Chart */}
          <Card className="lg:col-span-2 shadow-sm border-slate-200 dark:border-slate-800">
            <CardHeader>
              <CardTitle>Global Feature Importance</CardTitle>
              <CardDescription>
                Top biomarkers contributing to the diagnosis model based on training data.
              </CardDescription>
            </CardHeader>
            <CardContent className="h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={featureImportanceData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#e2e8f0" />
                  <XAxis type="number" hide />
                  <YAxis type="category" dataKey="name" width={140} tick={{fontSize: 12, fill: '#64748b'}} interval={0} />
                  <Tooltip 
                    cursor={{fill: 'transparent'}}
                    contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={32}>
                    {featureImportanceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Workflow Steps */}
          <Card className="shadow-sm border-slate-200 dark:border-slate-800">
            <CardHeader>
              <CardTitle>System Workflow</CardTitle>
              <CardDescription>Automated diagnostic pipeline</CardDescription>
            </CardHeader>
            <CardContent className="space-y-8 pt-6">
              
              <div className="flex items-start gap-4 relaltive group">
                <div className="bg-blue-100 dark:bg-blue-900/30 p-2.5 rounded-xl shadow-sm text-blue-600 dark:text-blue-400">
                  <FileText className="h-5 w-5" />
                </div>
                <div>
                  <h4 className="font-semibold text-sm">1. Upload Transcript</h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                    Upload a .cha file containing the patient interview transcript and timing.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 group">
                <div className="bg-purple-100 dark:bg-purple-900/30 p-2.5 rounded-xl shadow-sm text-purple-600 dark:text-purple-400">
                  <BarChart3 className="h-5 w-5" />
                </div>
                <div>
                  <h4 className="font-semibold text-sm">2. Feature Extraction</h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                    Python engine extracts pause duration, speech rate, and silence patterns.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 group">
                <div className="bg-green-100 dark:bg-green-900/30 p-2.5 rounded-xl shadow-sm text-green-600 dark:text-green-400">
                  <Brain className="h-5 w-5" />
                </div>
                <div>
                  <h4 className="font-semibold text-sm">3. RF Classification</h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                    Random Forest model predicts diagnosis (Control vs MCI) with biomarkers.
                  </p>
                </div>
              </div>

            </CardContent>
          </Card>
        </div>

        {/* Live Predictor Section */}
        <section className="pt-4" id="predict">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold tracking-tight">New Patient Analysis</h2>
            <Badge className="bg-indigo-600 hover:bg-indigo-700 text-white border-0">Live Model</Badge>
          </div>
          
          <Card className="bg-white dark:bg-slate-950 border-slate-200 dark:border-slate-800 shadow-md overflow-hidden">
            <CardContent className="p-0">
              <div className="grid grid-cols-1 md:grid-cols-2">
                
                {/* Left Side: Upload & Input */}
                <div className="p-8 border-r border-slate-100 dark:border-slate-800">
                  <form onSubmit={handlePredict} className="space-y-6">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        Upload Patient Transcript (.cha)
                      </label>
                      <div className="flex items-center justify-center w-full">
                        <label className={`flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${file ? 'border-green-300 bg-green-50 dark:bg-green-900/10' : 'border-slate-300 hover:bg-slate-50 dark:border-slate-700 dark:hover:bg-slate-900'}`}>
                          <div className="flex flex-col items-center justify-center pt-5 pb-6">
                            {file ? (
                              <>
                                <FileText className="w-10 h-10 mb-3 text-green-500" />
                                <p className="mb-2 text-sm text-green-600 font-semibold">{file.name}</p>
                                <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(1)} KB</p>
                              </>
                            ) : (
                              <>
                                <Upload className="w-10 h-10 mb-3 text-slate-400" />
                                <p className="mb-2 text-sm text-slate-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                                <p className="text-xs text-slate-500">Supported format: .cha (CHAT transcript)</p>
                              </>
                            )}
                          </div>
                          <input 
                            type="file" 
                            className="hidden" 
                            accept=".cha" 
                            onChange={handleFileChange}
                          />
                        </label>
                      </div>
                    </div>

                    {error && (
                      <Alert variant="destructive">
                        <AlertTriangle className="h-4 w-4" />
                        <AlertTitle>Error</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                      </Alert>
                    )}

                    <Button 
                      type="submit" 
                      className="w-full h-12 text-base font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-200 dark:shadow-none transition-all"
                      disabled={loading || !file}
                    >
                      {loading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Analyzing Transcript...
                        </>
                      ) : (
                        <>
                          <Activity className="mr-2 h-4 w-4" />
                          Analyze Patient
                        </>
                      )}
                    </Button>
                  </form>

                  <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 p-5 rounded-xl border border-blue-100 dark:border-blue-800">
                    <h4 className="font-semibold text-blue-900 dark:text-blue-100 flex items-center gap-2 mb-2">
                      <Clock className="w-4 h-4" />
                      Clinical Context
                    </h4>
                    <p className="text-sm text-blue-800 dark:text-blue-200 leading-relaxed opacity-90">
                      The model analyzes pause frequency and duration. Increased pause counts (&gt;1000) and reduced speech rates are strong indicators of MCI in the training dataset.
                    </p>
                  </div>
                </div>

                {/* Right Side: Results */}
                <div className="p-8 bg-slate-50 dark:bg-slate-900/50 flex flex-col justify-center min-h-[500px]">
                  {!prediction && !loading ? (
                    <div className="text-center space-y-4 text-slate-400">
                      <div className="bg-slate-100 dark:bg-slate-800 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                        <Brain className="w-8 h-8 opacity-50" />
                      </div>
                      <p className="text-sm font-medium">Upload a transcript to view diagnostic analysis</p>
                    </div>
                  ) : loading ? (
                    <div className="space-y-6 w-full max-w-sm mx-auto">
                        <div className="flex flex-col items-center justify-center space-y-4">
                            <Loader2 className="h-10 w-10 animate-spin text-blue-500" />
                            <p className="text-sm text-slate-500 font-medium">Extracting pause features...</p>
                        </div>
                      <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-full animate-pulse"></div>
                      <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-3/4 animate-pulse"></div>
                      <div className="h-32 bg-slate-200 dark:bg-slate-800 rounded animate-pulse mt-8"></div>
                    </div>
                  ) : (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 w-full">
                      
                      {/* Diagnosis Badge */}
                      <div className="text-center space-y-2">
                        <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Prediction Results</p>
                        <h3 className={`text-4xl font-bold ${prediction.predicted_diagnosis === 'Control' ? 'text-green-600' : 'text-amber-600'}`}>
                          {prediction.predicted_diagnosis}
                        </h3>
                        <Badge variant="outline" className={`${prediction.predicted_diagnosis === 'Control' ? 'bg-green-100 text-green-700 border-green-200' : 'bg-amber-100 text-amber-700 border-amber-200'} text-sm py-1 px-4`}>
                          Confidence: {prediction.confidence.toFixed(1)}%
                        </Badge>
                      </div>

                      {/* Extracted Features List */}
                      {extractedFeatures && (
                        <div className="bg-white dark:bg-slate-950 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
                            <h4 className="font-semibold text-sm mb-4 flex items-center gap-2">
                            <FileText className="w-4 h-4 text-slate-500" />
                            Extracted Biomarkers
                            </h4>
                            <div className="space-y-3">
                            <div className="flex justify-between items-center text-sm py-1 border-b border-slate-100 dark:border-slate-900">
                                <span className="text-slate-600 dark:text-slate-400">Pause Count</span>
                                <span className="font-mono font-medium">{extractedFeatures.pause_count}</span>
                            </div>
                            <div className="flex justify-between items-center text-sm py-1 border-b border-slate-100 dark:border-slate-900">
                                <span className="text-slate-600 dark:text-slate-400">Total Pause Time</span>
                                <span className="font-mono font-medium">{extractedFeatures.total_pause_time}s</span>
                            </div>
                            <div className="flex justify-between items-center text-sm py-1 border-b border-slate-100 dark:border-slate-900">
                                <span className="text-slate-600 dark:text-slate-400">Speech Rate</span>
                                <span className="font-mono font-medium">{extractedFeatures.speech_rate_wpm} WPM</span>
                            </div>
                            <div className="flex justify-between items-center text-sm py-1">
                                <span className="text-slate-600 dark:text-slate-400">Pause/Word Ratio</span>
                                <span className="font-mono font-medium">{extractedFeatures.pause_per_word_ratio}</span>
                            </div>
                            </div>
                        </div>
                      )}

                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>
    </div>
  );
}
